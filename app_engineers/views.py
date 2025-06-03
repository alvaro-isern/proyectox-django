from rest_framework import viewsets, permissions
from rest_framework import viewsets
from app_persons.models import Person, Contact
from app_engineers.models import Engineer
from app_engineers.serializers.person_serializer import PersonSerializer
from app_engineers.serializers.contact_serializer import ContactSerializer
from app_engineers.serializers.engineer_serializer import EngineerSerializer
# from app_engineers.serializers.document_type import DocumentTypeSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']

class EngineerViewSet(viewsets.ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer
    ordering_fields = '__all__'
    ordering = ['-created_at']



# class DocumentTypeViewSet(viewsets.ModelViewSet):
#     queryset = DocumentType.objects.all()
#     serializer_class = DocumentTypeSerializer
#     ordering_fields = '__all__'
#     ordering = ['-created_at']