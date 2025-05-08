from rest_framework import viewsets, permissions
from rest_framework import viewsets
from app_engineers.models import Person
from app_engineers.serializers.person_serializer import PersonSerializer
# from app_engineers.serializers.document_type import DocumentTypeSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']

# class DocumentTypeViewSet(viewsets.ModelViewSet):
#     queryset = DocumentType.objects.all()
#     serializer_class = DocumentTypeSerializer
#     ordering_fields = '__all__'
#     ordering = ['-created_at']