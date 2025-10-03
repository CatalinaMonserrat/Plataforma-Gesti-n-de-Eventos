from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Evento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginBootstrapForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre','fecha','ubicacion', 'asistentes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control'}),
            'asistentes': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        }