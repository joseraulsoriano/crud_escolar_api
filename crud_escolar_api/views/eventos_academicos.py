from rest_framework import generics
from crud_escolar_api.models import EventoAcademico
from crud_escolar_api.serializers import EventoAcademicoSerializer

class EventoAcademicoListCreateView(generics.ListCreateAPIView):
    queryset = EventoAcademico.objects.all().order_by('-fecha_realizacion')
    serializer_class = EventoAcademicoSerializer

class EventoAcademicoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventoAcademico.objects.all()
    serializer_class = EventoAcademicoSerializer 