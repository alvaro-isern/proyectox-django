#from rest_framework import viewsets, permissions
from rest_framework import viewsets
from app_ingenieros.models import Colegiado as Members, Ingeniero as Engineers, TipoDocumento as DocumentType
from app_ingenieros.serializers.members import MembersSerializer
from app_ingenieros.serializers.engineers import EngineerSerializer
from app_ingenieros.serializers.document_type import DocumentTypeSerializer
from rest_framework import filters
class MembersViewSet(viewsets.ModelViewSet):
    queryset = Members.objects.all()
    serializer_class = MembersSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']

class EngineersViewSet(viewsets.ModelViewSet):
    queryset = Engineers.objects.select_related('tipo_documento', 'pais').all()
    serializer_class = EngineerSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']
    filter_backends = [filters.SearchFilter]
    search_fields = ['ingeniero__nombres', 'ingeniero__apellidos', 'tipo_documento__tipo']

class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']
    filter_backends = [filters.SearchFilter]
    search_fields = ['tipo']