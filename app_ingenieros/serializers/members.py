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
    mobile = serializers.CharField()

    # Campos del colegiado
    status = serializers.IntegerField(read_only=True)
    chapter = serializers.IntegerField()
    departmental_council = serializers.IntegerField()
    collegiate_code = serializers.CharField()
    collegiate_type = serializers.IntegerField()

    class Meta:
        model = Colegiado
        fields = [
            'id', 'apellido_paterno', 'apellido_materno', 'nombres',
            'tipo_documento', 'numero_documento', 'correo', 'codigo_pais', 'celular',
            'estado_activo', 'capitulo', 'consejo_departamental', 'colegiatura',
            'tipo_colegiado'
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
            'tipo_documento': (TipoDocumento, "Tipo de documento no válido."),
            'codigo_pais': (Pais, "País no válido."),
            'capitulo': (Capitulo, "Capítulo no válido."),
            'tipo_colegiado': (TipoColegiado, "Tipo de colegiado no válido."),
            'consejo_departamental': (ConsejoDepartamental, "Consejo departamental no válido."),
            'colegiatura': (Colegiatura, "Colegiatura no válida.")
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

    def _get_ingeniero_data(self, validated_data, related_objects):
        """Prepara los datos del ingeniero"""
        return {
            'tipo_documento': related_objects['tipo_documento'],
            'pais': related_objects['codigo_pais'],
            'apellido_paterno': validated_data.pop('apellido_paterno'),
            'apellido_materno': validated_data.pop('apellido_materno'),
            'nombres': validated_data.pop('nombres'),
            'numero_documento': validated_data.pop('numero_documento'),
            'correo': validated_data.pop('correo'),
            'celular': validated_data.pop('celular')
        }

    def create(self, validated_data):
        # Obtener y validar objetos relacionados
        related_objects = self._get_related_objects(validated_data)

        # Obtener estado activo
        try:
            activo = Activo.objects.get(id=2)
        except Activo.DoesNotExist:
            raise serializers.ValidationError(
                {"estado_activo": "El estado no existe en la base de datos."}
            )

        # Crear o actualizar ingeniero
        ingeniero_data = self._get_ingeniero_data(
            validated_data, related_objects)
        ingeniero, _ = Ingeniero.objects.update_or_create(
            numero_documento=ingeniero_data['numero_documento'],
            defaults=ingeniero_data
        )

        # Crear colegiado
        return Colegiado.objects.create(
            ingeniero=ingeniero,
            capitulo=related_objects['capitulo'],
            tipo_colegiado=related_objects['tipo_colegiado'],
            consejo_departamental=related_objects['consejo_departamental'],
            colegiatura=related_objects['colegiatura'],
            activo=activo
        )

    def to_representation(self, instance):
        """Representación personalizada del objeto para el formulario"""
        ingeniero = instance.ingeniero
        return {
            'id': instance.id,
            'estado_activo': getattr(instance.activo, 'id', None),
            'apellido_paterno': ingeniero.apellido_paterno,
            'apellido_materno': ingeniero.apellido_materno,
            'nombres': ingeniero.nombres,
            'tipo_documento': getattr(ingeniero.tipo_documento, 'id', None),
            'numero_documento': ingeniero.numero_documento,
            'correo': ingeniero.correo,
            'codigo_pais': getattr(ingeniero.pais, 'id', None),
            'celular': ingeniero.celular,
            'capitulo': getattr(instance.capitulo, 'id', None),
            'consejo_departamental': getattr(instance.consejo_departamental, 'id', None),
            'colegiatura': getattr(instance.colegiatura, 'id', None),
            'tipo_colegiado': getattr(instance.tipo_colegiado, 'id', None)
        }

    def update(self, instance, validated_data):
        # Actualizar datos del ingeniero
        ingeniero_data = {}
        ingeniero_fields = {
            'tipo_documento': (TipoDocumento, "Tipo de documento no válido."),
            'codigo_pais': (Pais, "País no válido."),
            'apellido_paterno': None,
            'apellido_materno': None,
            'nombres': None,
            'numero_documento': None,
            'correo': None,
            'celular': None
        }

        for field, validation in ingeniero_fields.items():
            if field in validated_data:
                if validation:  # Si hay validación definida
                    model_class, error_message = validation
                    value = self.validate_required_field(
                        field, validated_data.pop(field), model_class, error_message)
                    ingeniero_data[field if field !=
                                   'codigo_pais' else 'pais'] = value
                else:  # Si no hay validación, usar el valor directamente
                    ingeniero_data[field] = validated_data.pop(field)

        if ingeniero_data:
            for key, value in ingeniero_data.items():
                setattr(instance.ingeniero, key, value)
            instance.ingeniero.save()

        # Actualizar campos del colegiado
        colegiado_fields = {
            'capitulo': (Capitulo, "Capítulo no válido."),
            'tipo_colegiado': (TipoColegiado, "Tipo de colegiado no válido."),
            'consejo_departamental': (ConsejoDepartamental, "Consejo departamental no válido."),
            'colegiatura': (Colegiatura, "Colegiatura no válida.")
        }

        for field, (model_class, error_message) in colegiado_fields.items():
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
            inactivo = Activo.objects.get(id=1)
        except Activo.DoesNotExist:
            raise serializers.ValidationError(
                {"estado_activo": "El estado no existe en la base de datos."}
            )

        instance.delete_logical()
        return True