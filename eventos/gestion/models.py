from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200, blank=True)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_organizados')
    asistentes = models.ManyToManyField(User, related_name='eventos_asistidos', blank=True)

    def __str__(self): return self.nombre
    def get_absolute_url(self): return reverse('evento_detail', kwargs={'pk': self.pk})
