from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import models
from django.contrib.auth import login

from .models import Evento
from .forms import EventoForm, SignUpForm


# ---------- Handler 403 (acceso denegado) ----------
def acceso_denegado(request, exception=None):
    return render(request, 'acceso_denegado.html', status=403)


class AccesoDenegadoView(TemplateView):
    template_name = 'acceso_denegado.html'


# ---------- Mixins ----------
class CustomPermissionMixin(PermissionRequiredMixin):
    """Muestra mensaje y redirige cuando faltan permisos."""
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para realizar esta acción.")
        return redirect('acceso_denegado')


class OwnerOrAdminMixin(UserPassesTestMixin):
    """Permite la acción solo a superuser/staff o al organizador del evento."""
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        return u.is_superuser or u.is_staff or obj.organizador_id == u.id

    def handle_no_permission(self):
        messages.error(self.request, "Solo el organizador o un administrador puede modificar este evento.")
        return redirect('acceso_denegado')


# ---------- Auth: Registro ----------
class SignUpView(FormView):
    template_name = 'registro/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('evento_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # inicia sesión tras registrarse
        messages.success(self.request, "¡Registro exitoso, bienvenida/o!")
        return super().form_valid(form)


# ---------- Vistas de Eventos ----------
class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'evento_list.html'
    context_object_name = 'eventos'
    ordering = ['fecha']

    def get_queryset(self):
        u = self.request.user
        qs = Evento.objects.all()
        if u.is_staff or u.is_superuser:
            return qs.order_by('fecha')
        # organizador o asistente
        return qs.filter(models.Q(organizador=u) | models.Q(asistentes=u)).distinct().order_by('fecha')


from django.core.exceptions import PermissionDenied
class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'evento_detail.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        u = request.user
        if u.is_staff or u.is_superuser or obj.organizador_id == u.id or obj.asistentes.filter(id=u.id).exists():
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "No puedes ver este evento (no estás registrado).")
        return redirect('acceso_denegado')


class EventoCreateView(LoginRequiredMixin, CustomPermissionMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'evento_form.html'
    permission_required = 'gestion.add_evento'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('asistentes', None)  # organizador los agrega luego
        return form
    
    def form_valid(self, form):
        form.instance.organizador = self.request.user
        messages.success(self.request, "¡Evento creado!")
        return super().form_valid(form)


class EventoUpdateView(LoginRequiredMixin, CustomPermissionMixin, OwnerOrAdminMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'evento_form.html'
    permission_required = 'gestion.change_evento'

    def form_valid(self, form):
        messages.success(self.request, "Evento actualizado.")
        return super().form_valid(form)


class EventoDeleteView(LoginRequiredMixin, CustomPermissionMixin, OwnerOrAdminMixin, DeleteView):
    model = Evento
    template_name = 'evento_confirm_delete.html'
    success_url = reverse_lazy('evento_list')
    permission_required = 'gestion.delete_evento'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Evento eliminado.")
        return super().delete(request, *args, **kwargs)