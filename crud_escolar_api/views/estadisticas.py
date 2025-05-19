from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from crud_escolar_api.models import Administradores, Maestros, Alumnos, EventoAcademico
from crud_escolar_api.serializers import EstadisticasGeneralesSerializer
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class EstadisticasGeneralesView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EstadisticasGeneralesSerializer

    def get(self, request, *args, **kwargs):
        # Obtener totales de usuarios
        total_admins = Administradores.objects.filter(user__is_active=1).count()
        total_maestros = Maestros.objects.filter(user__is_active=1).count()
        total_alumnos = Alumnos.objects.filter(user__is_active=1).count()

        # Obtener estadísticas de eventos por mes (últimos 6 meses)
        fecha_inicio = datetime.now().date() - timedelta(days=180)  # 6 meses atrás
        
        # Para debugging
        total_eventos = EventoAcademico.objects.count()
        logger.info(f"Total de eventos en la base de datos: {total_eventos}")
        
        eventos_por_mes_query = EventoAcademico.objects.filter(
            fecha_realizacion__gte=fecha_inicio
        ).annotate(
            mes=TruncMonth('fecha_realizacion')
        ).values('mes').annotate(
            total=Count('id')
        ).order_by('mes')
        
        logger.info(f"Query de eventos por mes: {eventos_por_mes_query.query}")
        
        # Convertir QuerySet a lista de diccionarios con formato de mes
        eventos_mes = []
        
        # Si no hay eventos por mes en la BD, generamos datos de ejemplo temporales
        if not eventos_por_mes_query.exists():
            # Generar datos de ejemplo para probar las gráficas
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
            for i, mes in enumerate(meses):
                eventos_mes.append({
                    'fecha': mes,
                    'total': i % 3 + 1  # Número aleatorio entre 1 y 3
                })
        else:
            for evento in eventos_por_mes_query:
                eventos_mes.append({
                    'fecha': evento['mes'].strftime('%B'),  # Nombre del mes
                    'total': evento['total']
                })

        # Obtener conteo de eventos por tipo
        eventos_por_tipo_query = EventoAcademico.objects.values(
            'tipo_evento'
        ).annotate(
            total=Count('id')
        ).order_by('tipo_evento')
        
        logger.info(f"Query de eventos por tipo: {eventos_por_tipo_query.query}")
        
        # Si no hay eventos por tipo en la BD, generamos datos de ejemplo temporales
        if not eventos_por_tipo_query.exists():
            # Generar datos de ejemplo para probar las gráficas
            tipos = ["Conferencia", "Taller", "Seminario", "Concurso"]
            eventos_por_tipo = [
                {'tipo_evento': tipo, 'total': i % 4 + 1} for i, tipo in enumerate(tipos)
            ]
        else:
            eventos_por_tipo = list(eventos_por_tipo_query)

        data = {
            'total_administradores': total_admins,
            'total_maestros': total_maestros,
            'total_alumnos': total_alumnos,
            'eventos_por_mes': eventos_mes,
            'eventos_por_tipo': eventos_por_tipo
        }
        
        logger.info(f"Datos enviados: {data}")

        serializer = self.get_serializer(data)
        return Response(serializer.data) 