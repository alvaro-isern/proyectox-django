from rest_framework import viewsets, permissions
from rest_framework import viewsets
from app_ingenieros.models import Member, Person, DocumentType
from app_ingenieros.serializers.members import MembersSerializer
from app_ingenieros.serializers.engineers import EngineerSerializer
from app_ingenieros.serializers.document_type import DocumentTypeSerializer


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MembersSerializer
    ordering_fields = '__all__'


class EngineersViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = EngineerSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']