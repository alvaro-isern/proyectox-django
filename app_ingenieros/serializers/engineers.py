from rest_framework import serializers
from app_ingenieros.models import Ingeniero
from app_ingenieros.models import TipoDocumento

class EngineerSerializer(serializers.ModelSerializer):

    tipo_documento_tipo = serializers.ChoiceField(choices=TipoDocumento.DOCUMENT_TYPE_CHOICES, source='tipo_documento.tipo')
    #pais_nombre = serializers.ChoiceField(source='pais.nombre', read_only=True)
    class Meta:
        model = Ingeniero
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate(self, data):
        """
        Validate the data before creating or updating an Ingeniero instance.
        """
        # Example validation: Ensure 'name' is not empty
        if not data.get('name'):
            raise serializers.ValidationError("Name field cannot be empty.")
        
        # Add any other custom validation logic here
        
        return data
    
    def create(self, validated_data):
        """
        Create a new Ingeniero instance.
        """
        instance = super().create(validated_data)
        # Add any post-creation logic here if needed
        return instance