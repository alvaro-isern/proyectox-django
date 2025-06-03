from rest_framework import serializers
from app_engineers.models import Engineer
from app_persons.models import Person
from .person_serializer import PersonSerializer

class EngineerSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Engineer."""
    person = PersonSerializer()

    class Meta:
        model = Engineer
        fields = [
            'id',
            'is_active',
            'colligiate_code',
            'person',
            # 'specialty',
            'registration_date',
            'member_type',
            'vitalicio_date',
            'departament_council',
        ]
        read_only_fields = ['id', 'is_active']

    def create(self, validated_data):
        """Crear una nueva instancia de Engineer."""
        person_data = validated_data.pop('person')
        person_serializer = PersonSerializer(data=person_data)
        person_serializer.is_valid(raise_exception=True)
        person = person_serializer.save()

        engineer = Engineer.objects.create(
            person=person,
            **validated_data
        )
        return engineer

    def update(self, instance, validated_data):
        """Actualizar una instancia existente de Engineer."""
        person_data = validated_data.pop('person', None)
        
        # Actualizar los campos de Engineer
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar los datos de Person si se proporcionan
        if person_data:
            person_serializer = PersonSerializer(
                instance.person, data=person_data, partial=True)
            person_serializer.is_valid(raise_exception=True)
            person_serializer.save()

        return instance
