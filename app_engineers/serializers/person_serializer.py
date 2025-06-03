from urllib.parse import urlparse

# from app_engineers.services.ImageController import HybridImageField
import requests
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app_persons.models import Person, Contact, Country
from .contact_serializer import ContactSerializer


# from django.conf import settings

class URLImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if data == "" or data is None:
            return None

        return super().to_internal_value(data)


class PersonSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Person."""
    contact = ContactSerializer(many=True, read_only=True, source='contacts')
    civil_state = serializers.CharField(required=False, allow_blank=True)
    photo = URLImageField(required=False)

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
    contact_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Person
        fields = [
            'id',
            'is_active',
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
            'contact_id',
            'cellphone',
            'email',
            'address',
            'use',
            'is_main',
        ]
        read_only_fields = ['id', 'is_active', 'person']

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
        # Agregar la URL completa para el campo photo
        if representation.get('photo'):
            request = self.context.get('request')
            if request:
                representation['photo'] = request.build_absolute_uri(
                    representation['photo'])
            else:
                representation['photo'] = f"http://127.0.0.1:8000{representation['photo']}"
        
        # Remove person field from contacts
        if representation.get('contact'):
            for contact in representation['contact']:
                contact.pop('person', None)
                
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

        with transaction.atomic():
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

            try:
                Contact.objects.create(
                    person=person,
                    **contact_data
                )
            except Exception as e:
                raise serializers.ValidationError(
                    {"contact": f"Error al crear el contacto: {str(e)}"})

        return person

    def update(self, instance, validated_data):
        """Actualizar una instancia existente de Person."""
        # Extraer los datos del contacto del validated_data
        contact_fields = ['cellphone', 'email',
                          'address', 'use', 'is_main']
        contact_data = {}
        contact_id = validated_data.pop('contact_id', None)

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

        with transaction.atomic():
            # Actualizar los campos de Person
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Actualizar el contacto específico si se proporciona un ID
            if contact_id is not None:
                try:
                    contact = Contact.objects.get(id=contact_id, person=instance)
                    for attr, value in contact_data.items():
                        setattr(contact, attr, value)
                    contact.save()
                except Contact.DoesNotExist:
                    raise serializers.ValidationError(
                        {"contact_id": "El contacto especificado no existe para esta persona."}
                    )
            else:
                # Si no se proporciona ID, actualizar o crear el contacto principal
                contact, created = Contact.objects.update_or_create(
                    person=instance,
                    defaults=contact_data
                )

        return instance
