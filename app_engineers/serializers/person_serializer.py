from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app_engineers.models import Person, Contact, Country
# from app_engineers.services.ImageController import HybridImageField
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse


# from django.conf import settings

class URLImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if data == "" or data is None:
            return None

        return super().to_internal_value(data)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'cellphone', 'email', 'address', 'use', 'is_main']
        read_only_fields = ['id']

class PersonSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Person."""
    # person attributes
    names = serializers.CharField(required=True)
    paternal_surname = serializers.CharField(required=True)
    maternal_surname = serializers.CharField(required=True)
    doc_number = serializers.CharField(required=True)
    contact = ContactSerializer(required=False, read_only=True)
    birth_date = serializers.DateField(required=False)
    civil_state = serializers.CharField(required=False, allow_blank=True)
    photo = URLImageField(
        required=False)
    document_type = serializers.IntegerField(required=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), required=True)

    # Contact fields (write_only)
    cellphone = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    email = serializers.EmailField(
        write_only=True, required=False, allow_blank=True)
    address = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    use = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    is_main = serializers.CharField(
        write_only=True, required=False, allow_blank=True)

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
            'country',
            'cellphone',
            'email',
            'address',
            'use',
            'is_main'
        ]
        read_only_fields = ['id']

    def validate_photo(self, value):
        # Si el valor ya es un archivo (ContentFile u otro), no realizar más validaciones
        if hasattr(value, 'read'):
            return value

        if not value or value == "":
            return None

        # Si es una URL completa, descargar la imagen
        if isinstance(value, str) and value.startswith(('http://', 'https://')):
            try:
                response = requests.get(value)
                if response.status_code == 200:
                    # Validar que el contenido sea una imagen
                    content_type = response.headers.get('Content-Type', '')
                    if not content_type.startswith('image/'):
                        raise serializers.ValidationError(
                            "La URL no contiene una imagen válida."
                        )

                    # Obtener el nombre del archivo de la URL
                    filename = urlparse(value).path.split('/')[-1]
                    return ContentFile(response.content, name=filename)
                else:
                    raise serializers.ValidationError(
                        "No se pudo descargar la imagen de la URL proporcionada."
                    )
            except Exception as e:
                raise serializers.ValidationError(
                    f"Error al descargar la imagen: {str(e)}"
                )

        return value

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

        # Agregar la URL completa para el campo photo
        if representation.get('photo'):
            request = self.context.get('request')
            if request:
                representation['photo'] = request.build_absolute_uri(
                    representation['photo'])
            else:
                representation['photo'] = f"http://127.0.0.1:8000{representation['photo']}"
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

    def to_internal_value(self, data):
        # Sobrescribir el manejo del campo 'photo' para aceptar URLs
        if 'photo' in data and isinstance(data['photo'], str) and data['photo'].startswith(('http://', 'https://')):
            try:
                response = requests.get(data['photo'], stream=True)
                if response.status_code == 200:
                    # Validar que el contenido sea una imagen
                    content_type = response.headers.get('Content-Type', '')
                    if not content_type.startswith('image/'):
                        raise ValidationError(
                            {"photo": "La URL no contiene una imagen válida."})

                    # Descargar la imagen y convertirla en un archivo
                    filename = urlparse(data['photo']).path.split('/')[-1]
                    data['photo'] = ContentFile(
                        response.content, name=filename)
                else:
                    raise ValidationError(
                        {"photo": "No se pudo descargar la imagen de la URL proporcionada."})
            except Exception as e:
                raise ValidationError(
                    {"photo": f"Error al descargar la imagen: {str(e)}"})

        return super().to_internal_value(data)

    def create(self, validated_data):
        """Crear una nueva instancia de Person."""
        # Extraer los datos del contacto del validated_data
        contact_fields = ['cellphone', 'email', 'address', 'use', 'is_main']
        contact_data = {}

        for field in contact_fields:
            value = validated_data.pop(field, None)
            if value == "":
                contact_data[field] = None
            else:
                contact_data[field] = value

        # Manejar campos vacíos de Person
        if validated_data.get('civil_state') == "":
            validated_data['civil_state'] = None
        if validated_data.get('photo') == "":
            validated_data['photo'] = None

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
