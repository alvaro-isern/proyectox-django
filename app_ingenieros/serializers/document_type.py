from rest_framework import serializers
from app_ingenieros.models import TipoDocumento as DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'tipo']
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
        if not data.get('tipo'):
            raise serializers.ValidationError("Tipo field cannot be empty.")
        
        # Add any other custom validation logic here
        
        return data
