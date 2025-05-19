from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from crud_escolar_api.models import Administradores, Maestros, Alumnos, EventoAcademico, EstadisticasEventos
from crud_escolar_api.serializers import EstadisticasGeneralesSerializer
from datetime import datetime, timedelta

class EstadisticasGeneralesView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EstadisticasGeneralesSerializer

    def get(self, request, *args, **kwargs):
        # Obtener totales de usuarios
        total_admins = Administradores.objects.filter(user__is_active=1).count()
        total_maestros = Maestros.objects.filter(user__is_active=1).count()
        total_alumnos = Alumnos.objects.filter(user__is_active=1).count()

        # Obtener estadísticas de eventos por día (últimos 7 días)
        fecha_inicio = datetime.now().date() - timedelta(days=6)
        eventos_por_dia = EventoAcademico.objects.filter(
            fecha_realizacion__gte=fecha_inicio
        ).annotate(
            fecha=TruncDate('fecha_realizacion')
        ).values('fecha').annotate(
            total=Count('id')
        ).order_by('fecha')

        # Convertir QuerySet a lista de diccionarios
        eventos_dia = []
        fecha_actual = fecha_inicio
        for _ in range(7):
            evento = next(
                (e for e in eventos_por_dia if e['fecha'] == fecha_actual),
                {'fecha': fecha_actual, 'total': 0}
            )
            eventos_dia.append({
                'fecha': evento['fecha'].strftime('%a'),
                'total': evento['total']
            })
            fecha_actual += timedelta(days=1)

        # Obtener estadísticas por tipo de evento
        eventos_por_tipo = EventoAcademico.objects.values(
            'tipo_evento'
        ).annotate(
            total=Count('id')
        ).order_by('tipo_evento')

        data = {
            'total_administradores': total_admins,
            'total_maestros': total_maestros,
            'total_alumnos': total_alumnos,
            'eventos_por_dia': eventos_dia,
            'eventos_por_tipo': list(eventos_por_tipo)
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data) 