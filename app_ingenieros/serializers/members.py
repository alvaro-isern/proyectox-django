from rest_framework import serializers
from app_ingenieros.models import Colegiado

class MembersSerializer(serializers.ModelSerializer):
    """
    Serializer for the Colegiado model with custom validations.
    """

    class Meta:
        model = Colegiado
        fields = [
            'id', 
            'ingeniero', 
            'colegiatura', 
            'tipo_colegiado', 
            'consejo_departamental', 
            'capitulo', 
            'activo'
        ]
        read_only_fields = ['id']  # Make 'id' read-only

    def validate_colegiatura(self, value):
        """
        Field-level validation for 'colegiatura'.
        Ensures that the value is numeric.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Colegiatura must be numeric.")
        return value

    def validate(self, data):
        """
        Object-level validation.
        Ensures that 'colegiatura' is provided if 'activo' is True.
        """
        activo = data.get('activo')
        colegiatura = data.get('colegiatura')

        if activo and not colegiatura:
            raise serializers.ValidationError({
                'colegiatura': "Colegiatura is required if the member is active."
            })
        return data

    def create(self, validated_data):
        """
        Custom creation logic for the Colegiado instance.
        """
        instance = super().create(validated_data)
        # Add any post-creation logic here if needed
        return instance

    def update(self, instance, validated_data):
        """
        Custom update logic for the Colegiado instance.
        """
        instance = super().update(instance, validated_data)
        # Add any post-update logic here if needed
        return instance