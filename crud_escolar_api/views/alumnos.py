from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from crud_escolar_api.serializers import *
from crud_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

class AlumnosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active = 1).order_by("id")
        lista = AlumnoSerializer(alumnos, many=True).data
        
        return Response(lista, 200)
    
class AlumnosView(generics.CreateAPIView):
    #Obtener usuario por ID
    def get(self, request, *args, **kwargs):
        try:
            alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
            alumno = AlumnoSerializer(alumno, many=False).data
            return Response(alumno, 200)
        except Exception as e:
            return Response({"error": str(e)}, 404)
    
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            #Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)

            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            #Create a profile for the user
            alumno = Alumnos.objects.create(user=user,
                                            matricula= request.data["matricula"],
                                            curp= request.data["curp"].upper(),
                                            rfc= request.data["rfc"].upper(),
                                            fecha_nacimiento= request.data["fecha_nacimiento"],
                                            edad= request.data["edad"],
                                            telefono= request.data["telefono"],
                                            ocupacion= request.data["ocupacion"])
            alumno.save()

            return Response({"alumno_created_id": alumno.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class AlumnosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    #Actualizar alumno
    def put(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.data.get("id"))
        user = alumno.user
        
        #Actualizar datos del usuario
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.save()
        
        #Actualizar datos del alumno
        alumno.matricula = request.data.get("matricula", alumno.matricula)
        alumno.curp = request.data.get("curp", alumno.curp).upper()
        alumno.rfc = request.data.get("rfc", alumno.rfc).upper()
        alumno.fecha_nacimiento = request.data.get("fecha_nacimiento", alumno.fecha_nacimiento)
        alumno.edad = request.data.get("edad", alumno.edad)
        alumno.telefono = request.data.get("telefono", alumno.telefono)
        alumno.ocupacion = request.data.get("ocupacion", alumno.ocupacion)
        alumno.save()
        
        return Response({"message": "Alumno actualizado correctamente"}, 200)
    
    #Eliminar alumno
    def delete(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
        user = alumno.user
        
        #Desactivar usuario
        user.is_active = 0
        user.save()
        
        return Response({"message": "Alumno eliminado correctamente"}, 200)