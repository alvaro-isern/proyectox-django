from rest_framework import serializers
from app_ingenieros.models import (
    Member, Engineer, DocumentType, Country, Status,
    CollegiateType, DepartmentalCouncil, Chapter
)


class MembersSerializer(serializers.ModelSerializer):
    names = serializers.CharField()
    maternal_surname = serializers.CharField()
    paternal_surname = serializers.CharField()
    document_type = serializers.IntegerField()
    document_number = serializers.CharField()
    email = serializers.EmailField()
    country_code = serializers.IntegerField()
    cellphone = serializers.CharField()

    # Campos del colegiado
    status = serializers.IntegerField(read_only=True)
    chapter = serializers.IntegerField()
    departmental_council = serializers.IntegerField()
    collegiate_code = serializers.CharField()
    collegiate_type = serializers.IntegerField()

    class Meta:
        model = Member
        fields = [
            'id',
            'status',
            'names',
            'paternal_surname',
            'maternal_surname',
            'collegiate_code',
            'chapter',
            'departmental_council',
            'collegiate_type',
            'document_type',
            'document_number',
            'email',
            'country_code',
            'cellphone'
        ]
        read_only_fields = ['id']

    def validate_required_field(self, field_name, field_value, model_class, error_message):
        """Método auxiliar para validar campos requeridos"""
        if not field_value:
            raise serializers.ValidationError(
                {field_name: "Este campo es obligatorio."})
        try:
            return model_class.objects.get(id=field_value)
        except model_class.DoesNotExist:
            raise serializers.ValidationError({field_name: error_message})

    def _get_related_objects(self, validated_data):
        """Obtiene y valida todos los objetos relacionados"""
        fields_to_validate = {
            'document_type': (DocumentType, "Tipo de documento no válido."),
            'country_code': (Country, "País no válido."),
            'chapter': (Chapter, "Capítulo no válido."),
            'collegiate_type': (CollegiateType, "Tipo de colegiado no válido."),
            'departmental_council': (DepartmentalCouncil, "Consejo departamental no válido.")
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

    def _get_engineer_data(self, validated_data, related_objects):
        """Prepara los datos del ingeniero"""
        return {
            'documents_types': related_objects['document_type'],
            'countries': related_objects['country_code'],
            'paternal_surname': validated_data.pop('paternal_surname'),
            'maternal_surname': validated_data.pop('maternal_surname'),
            'names': validated_data.pop('names'),
            'doc_number': validated_data.pop('document_number'),
            'email': validated_data.pop('email'),
            'cellphone': validated_data.pop('cellphone'),
        }

    def create(self, validated_data):
        # Obtener y validar objetos relacionados
        related_objects = self._get_related_objects(validated_data)

        # Obtener estado active
        try:
            active = Status.objects.get(id=2)
        except Status.DoesNotExist:
            raise serializers.ValidationError(
                {"estado_activo": "El estado no existe en la base de datos."}
            )

        # Crear o actualizar ingeniero
        engineer_data = self._get_engineer_data(
            validated_data, related_objects)
        engineer, _ = Engineer.objects.update_or_create(
            numero_documento=engineer_data['doc_number'],
            defaults=engineer_data
        )

        # Crear colegiado
        return Member.objects.create(
            engineer=engineer,
            collegiate_code=validated_data.pop('collegiate_code'),
            chapter=related_objects['chapter'],
            collegiate_type=related_objects['collegiate_type'],
            departmental_council=related_objects['departmental_council'],
            status=active,
        )

    def to_representation(self, instance):
        """Representación personalizada del objeto para el formulario"""
        engineer = instance.engineer
        return {
            'id': instance.id,
            'status': getattr(instance.active, 'id', None),
            'collegiate_code': instance.collegiate_code,
            'paternal_surname': engineer.paternal_surname,
            'maternal_surname': engineer.maternal_surname,
            'names': engineer.names,
            'document_type': getattr(engineer.document_type, 'id', None),
            'document_number': engineer.doc_number,
            'email': engineer.email,
            'country_code': getattr(engineer.country, 'id', None),
            'cellphone': engineer.cellphone,
            'chapter': getattr(instance.chapter, 'id', None),
            'departmental_council': getattr(instance.departmental_council, 'id', None),
            'colligaite_type': getattr(instance.colligaite_type, 'id', None)
        }

    def update(self, instance, validated_data):
        # Actualizar datos del engineer
        engineer_data = {}
        engineer_fields = {
            'document_type': (DocumentType, "Tipo de documento no válido."),
            'country_code': (Country, "País no válido."),
            'paternal_surname': None,
            'maternal_surname': None,
            'names': None,
            'document_number': None,
            'email': None,
            'cellphone': None
        }

        for field, validation in engineer_fields.items():
            if field in validated_data:
                if validation:  # Si hay validación definida
                    model_class, error_message = validation
                    value = self.validate_required_field(
                        field, validated_data.pop(field), model_class, error_message)
                    engineer_data[field if field !=
                                  'codigo_pais' else 'pais'] = value
                else:  # Si no hay validación, usar el valor directamente
                    engineer_data[field] = validated_data.pop(field)

        if engineer_data:
            for key, value in engineer_data.items():
                setattr(instance.engineer, key, value)
            instance.engineer.save()

        # Actualizar campos del colegiado
        member_fields = {
            'chapter': (Chapter, "Capítulo no válido."),
            'collegiate_type': (CollegiateType, "Tipo de colegiado no válido."),
            'departmental_council': (DepartmentalCouncil, "Consejo departamental no válido."),
            'status': (Status, "Estado no válido.")
        }

        for field, (model_class, error_message) in member_fields.items():
            if field in validated_data:
                value = self.validate_required_field(
                    field,
                    validated_data.pop(field),
                    model_class,
                    error_message
                )
                setattr(instance, field, value)

        instance.save()
        return instance

    def destroy(self, instance):
        """Realiza una eliminación lógica del colegiado."""
        try:
            # Asumiendo que el estado inactivo tiene id=1
            inactive = Status.objects.get(id=1)
        except Status.DoesNotExist:
            raise serializers.ValidationError(
                {"status": "El estado no existe en la base de datos."}
            )

        instance.delete_logical()
        return True
