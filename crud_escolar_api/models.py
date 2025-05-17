from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.first_name+" "+self.last_name
    
class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255,null=True, blank=True)
    curp = models.CharField(max_length=255,null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del alumno "+self.first_name+" "+self.last_name

class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    cubiculo = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    area_investigacion = models.CharField(max_length=255,null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del maestro "+self.first_name+" "+self.last_name

class EventoAcademico(models.Model):
    TIPO_EVENTO_CHOICES = [
        ("Conferencia", "Conferencia"),
        ("Taller", "Taller"),
        ("Seminario", "Seminario"),
        ("Concurso", "Concurso"),
    ]
    PUBLICO_OBJETIVO_CHOICES = [
        ("Estudiantes", "Estudiantes"),
        ("Profesores", "Profesores"),
        ("Publico general", "Publico general"),
    ]
    PROGRAMA_EDUCATIVO_CHOICES = [
        ("Ingeniería en Ciencias de la Computación", "Ingeniería en Ciencias de la Computación"),
        ("Licenciatura en Ciencias de la Computación", "Licenciatura en Ciencias de la Computación"),
        ("Ingeniería en Tecnologías de la Información", "Ingeniería en Tecnologías de la Información"),
    ]
    nombre_evento = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES)
    fecha_realizacion = models.DateField()
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    lugar = models.CharField(max_length=100)
    publico_objetivo = models.CharField(max_length=20, choices=PUBLICO_OBJETIVO_CHOICES)
    programa_educativo = models.CharField(max_length=50, choices=PROGRAMA_EDUCATIVO_CHOICES, null=True, blank=True)
    responsable_maestro = models.ForeignKey('Maestros', null=True, blank=True, on_delete=models.SET_NULL, related_name='eventos_maestro')
    responsable_admin = models.ForeignKey('Administradores', null=True, blank=True, on_delete=models.SET_NULL, related_name='eventos_admin')
    descripcion_breve = models.CharField(max_length=300)
    cupo_maximo = models.PositiveIntegerField()
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_evento