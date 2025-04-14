from rest_framework import serializers
from app_ingenieros.models import Engineer

class EngineerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Engineer
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate(self, data):
        """
        Validate the data before creating or updating an Engineer instance.
        """
        # Example validation: Ensure 'name' is not empty
        if not data.get('names'):
            raise serializers.ValidationError("Name field cannot be empty.")
        
        # Add any other custom validation logic here
        
        return data
    
    def create(self, validated_data):
        """
        Create a new Ingeniero instance.
        """
        instance = super().create(validated_data)

        return instance
    
    def to_representation(self, instance):
        """Customize the serialized output."""
        representation = super().to_representation(instance)

        DocumentType = instance.document_type
        if DocumentType:
            representation['document_type'] = {
                'id': DocumentType.id,
                'type': DocumentType.doc_type
            }
        else:
            representation['document_type'] = None

        Country = instance.country
        if Country:
            representation['country'] = {
                'id': Country.id,
                'code': Country.country_cod,
                'iso_code': Country.iso_code,
                'name': Country.name
            }
        else:
            representation['country'] = None

        return representation