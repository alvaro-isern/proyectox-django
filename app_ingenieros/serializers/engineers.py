from rest_framework import serializers
from app_ingenieros.models import Ingeniero

class EngineerSerializer(serializers.ModelSerializer):
    
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
        if not data.get('nombres'):
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
    
    def to_representation(self, instance):
        """Customize the serialized output."""
        representation = super().to_representation(instance)

        TipoDocumento = instance.tipo_documento
        if TipoDocumento:
            representation['tipo_documento'] = {
                'id': TipoDocumento.id,
                'tipo': TipoDocumento.tipo
            }
        else:
            representation['tipo_documento'] = None

        Pais = instance.pais
        if Pais:
            representation['pais'] = {
                'id': Pais.id,
                'codigo': Pais.codigo,
                'nombre': Pais.nombre
            }
        else:
            representation['pais'] = None

        return representation