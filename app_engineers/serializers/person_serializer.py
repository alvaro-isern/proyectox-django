from rest_framework import serializers
from app_engineers.models import Person, Contact, Country

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','cellphone', 'email', 'address', 'use', 'is_main']
        read_only_fields = ['id']

class PersonSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Person."""
    # person attributes
    names = serializers.CharField(required=True)
    paternal_surname = serializers.CharField(required=True)
    maternal_surname = serializers.CharField(required=True)
    doc_number = serializers.CharField(required=True)
    contact = ContactSerializer(required=False)
    birth_date = serializers.DateField(required=False)
    civil_state = serializers.IntegerField(required=False)
    photo = serializers.ImageField(required=False)
    document_type = serializers.IntegerField(required=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True)

    class Meta:
        model = Person
        fields = [
            'id',
            'names',
            'paternal_surname',
            'maternal_surname',
            'civil_state',
            'doc_number',
            'contact',
            'photo',
            'birth_date',
            'document_type',
            'country'
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """Incluir los datos del contacto en la respuesta."""
        representation = super().to_representation(instance)
        try:
            contact = instance.contacts.first()  # Obtener el primer contacto
            if contact:
                representation['contact'] = ContactSerializer(contact).data
            else:
                representation['contact'] = None
        except Contact.DoesNotExist:
            representation['contact'] = None
        return representation

    def validate_required_field(self, field_name, field_value, model_class, error_message):
        """Validar si el campo es requerido y existe en el modelo."""
        if not field_value:
            raise serializers.ValidationError(
                {field_name: "Este campo es obligatorio."})
        try:
            return model_class.objects.get(id=field_value)
        except model_class.DoesNotExist:
            raise serializers.ValidationError({field_name: error_message})

    def _get_related_objects(self, validated_data):
        fields_to_validate = {
            'country': (Country, "Tipo de país no válido."),
        }

        result = {}
        for field, (model_class, error_message) in fields_to_validate.items():
            result[field] = self.validate_required_field(
                field,
                validated_data.pop(field, None),
                model_class,
                error_message
            )
        return result

    def create(self, validated_data):
        """Crear una nueva instancia de Person."""
        contact_data = validated_data.pop('contact', {})

        person = Person.objects.create(
            names=validated_data.pop('names'),
            paternal_surname=validated_data.pop('paternal_surname'),
            maternal_surname=validated_data.pop('maternal_surname'),
            doc_number=validated_data.pop('doc_number'),
            document_type=validated_data.pop('document_type'),
            country=validated_data.pop('country'),
            birth_date=validated_data.pop('birth_date', None),
            photo=validated_data.pop('photo', None),
            civil_state=validated_data.pop('civil_state', None),
        )

        # Crear el contacto y asociarlo con la persona
        contact = Contact.objects.create(
            person=person,
            **contact_data
        )

        return person
