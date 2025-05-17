from rest_framework import serializers
from rest_framework.authtoken.models import Token
from crud_escolar_api.models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class EventoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoAcademico
        fields = '__all__'

    def validate(self, data):
        responsable_maestro = data.get('responsable_maestro')
        responsable_admin = data.get('responsable_admin')
        if responsable_maestro and responsable_admin:
            raise serializers.ValidationError('Solo puede haber un responsable: maestro o administrador, no ambos.')
        if not responsable_maestro and not responsable_admin:
            raise serializers.ValidationError('Debe seleccionar un responsable: maestro o administrador.')
        return data