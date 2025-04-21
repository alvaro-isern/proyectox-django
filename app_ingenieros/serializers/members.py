from rest_framework import serializers
from app_ingenieros.models import (
    Member, MemberInfo, DocumentType, Country,
    CollegiateType, DepartmentalCouncil, Chapter
)


class MembersSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Member."""
    # person atributes
    names = serializers.CharField(required=True)
    paternal_surname = serializers.CharField(required=True)
    maternal_surname = serializers.CharField(required=True)
    document_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    cellphone = serializers.CharField(required=True)
    address = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    photo = serializers.ImageField(required=False)
    document_type = serializers.IntegerField(required=True)
    country_code = serializers.IntegerField(required=True)

    # user atributes
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # member atributes
    collegiate_code = serializers.CharField(required=True)

    # member info atributes
    chapter = serializers.IntegerField(required=True)
    departmental_council = serializers.IntegerField(required=True)
    collegiate_type = serializers.IntegerField(required=True)
    status = serializers.BooleanField(read_only=True)
    

    
    
    

    class Meta:
        model = Member
        fields = [
            'id',
            'status',
            'collegiate_code',
            'paternal_surname',
            'maternal_surname',
            'names',
            'document_type',
            'document_number',
            'country_code',
            'email',
            'cellphone',
            'photo',
            'birth_date',
            'address',
            'chapter',
            'departmental_council',
            'collegiate_type',
            'user_email',
            'username',
            'password',
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

    def _get_person_data(self, validated_data):
        """Prepara los datos de la persona"""
        return {
            'paternal_surname': validated_data.pop('paternal_surname'),
            'maternal_surname': validated_data.pop('maternal_surname'),
            'names': validated_data.pop('names'),
            'document_type': validated_data.pop('document_type'),
            'photo': validated_data.pop('photo', None),
            'birth_date': validated_data.pop('birth_date', None),
            'address': validated_data.pop('address', None),
            'doc_number': validated_data.pop('document_number'),
            'email': validated_data.pop('email', None),
            'country_code': validated_data.pop('country_code'),
            'cellphone': validated_data.pop('cellphone', None),
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
        }

    def create(self, validated_data):
        # Obtener y validar objetos relacionados
        related_objects = self._get_related_objects(validated_data)

        # Crear o actualizar ingeniero
        member_data = self._get_member_data(
            validated_data, related_objects)
        member, _ = MemberInfo.objects.update_or_create(
            numero_documento=member_data['doc_number'],
            defaults=member_data
        )

        # Crear colegiado
        return Member.objects.create(
            member=member,
            collegiate_code=validated_data.pop('collegiate_code'),
            chapter=related_objects['chapter'],
            collegiate_type=related_objects['collegiate_type'],
            departmental_council=related_objects['departmental_council'],
            status=active,
        )

    def to_representation(self, instance):
        """Representación personalizada del objeto para el formulario"""
        member = instance.member
        return {
            'id': instance.id,
            'status': getattr(instance.active, 'id', None),
            'collegiate_code': instance.collegiate_code,
            'paternal_surname': member.paternal_surname,
            'maternal_surname': member.maternal_surname,
            'names': member.names,
            'document_type': getattr(member.document_type, 'id', None),
            'document_number': member.doc_number,
            'email': member.email,
            'country_code': getattr(member.country, 'id', None),
            'cellphone': member.cellphone,
            'chapter': getattr(instance.chapter, 'id', None),
            'departmental_council': getattr(instance.departmental_council, 'id', None),
            'colligaite_type': getattr(instance.colligaite_type, 'id', None)
        }

    def update(self, instance, validated_data):
        # Actualizar datos del member
        member_data = {}
        member_fields = {
            'document_type': (DocumentType, "Tipo de documento no válido."),
            'country_code': (Country, "País no válido."),
            'paternal_surname': None,
            'maternal_surname': None,
            'names': None,
            'document_number': None,
            'email': None,
            'cellphone': None
        }

        for field, validation in member_fields.items():
            if field in validated_data:
                if validation:  # Si hay validación definida
                    model_class, error_message = validation
                    value = self.validate_required_field(
                        field, validated_data.pop(field), model_class, error_message)
                    member_data[field if field !=
                                'codigo_pais' else 'pais'] = value
                else:  # Si no hay validación, usar el valor directamente
                    member_data[field] = validated_data.pop(field)

        if member_data:
            for key, value in member_data.items():
                setattr(instance.member, key, value)
            instance.member.save()

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
