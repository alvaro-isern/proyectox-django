# from rest_framework import viewsets, permissions
# from rest_framework import viewsets
# from app_engineers.models import Member, DocumentType
# from app_engineers.serializers.members import MembersSerializer
# from app_engineers.serializers.document_type import DocumentTypeSerializer
#
#
# class MembersViewSet(viewsets.ModelViewSet):
#     queryset = Member.objects.all()
#     serializer_class = MembersSerializer
#     ordering_fields = '__all__'
#
# class DocumentTypeViewSet(viewsets.ModelViewSet):
#     queryset = DocumentType.objects.all()
#     serializer_class = DocumentTypeSerializer
#     ordering_fields = '__all__'
#     ordering = ['-created_at']