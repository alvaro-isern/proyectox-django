from rest_framework import serializers
from app_ingenieros.models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'doc_type']
        read_only_fields = ['id']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate(self, data):
        """
        Validate the data before creating or updating a DocumentType instance.
        """
        # Example validation: Ensure 'tipo' is not empty
        if not data.get('doc_type'):
            raise serializers.ValidationError("Document type field cannot be empty.")
        
        # Add any other custom validation logic here
        
        return data
