from rest_framework import serializers
from app_ingenieros.models import (
    Colegiado, Ingeniero, TipoDocumento, Pais, Activo,
    Colegiatura, Capitulo, TipoColegiado, ConsejoDepartamental
)


class MembersSerializer(serializers.ModelSerializer):
    nombres = serializers.CharField()
    apellido_materno = serializers.CharField()
    apellido_paterno = serializers.CharField()
    tipo_documento = serializers.IntegerField()
    numero_documento = serializers.CharField()
    correo = serializers.EmailField()
    codigo_pais = serializers.IntegerField()
    celular = serializers.CharField()
    estado_activo = serializers.IntegerField(read_only=True)
    capitulo = serializers.IntegerField()
    consejo_departamental = serializers.IntegerField()
    colegiatura = serializers.IntegerField()
    tipo_colegiado = serializers.IntegerField()

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
            raise serializers.ValidationError({field_name: "Este campo es obligatorio."})
        try:
            return model_class.objects.get(id=field_value)
        except model_class.DoesNotExist:
            raise serializers.ValidationError({field_name: error_message})

    def create(self, validated_data):
        # Validar y obtener objetos relacionados
        tipo_documento = self.validate_required_field(
            'tipo_documento', 
            validated_data.pop('tipo_documento', None),
            TipoDocumento,
            "Tipo de documento no válido."
        )

        pais = self.validate_required_field(
            'codigo_pais',
            validated_data.pop('codigo_pais', None),
            Pais,
            "País no válido."
        )

        capitulo = self.validate_required_field(
            'capitulo',
            validated_data.pop('capitulo', None),
            Capitulo,
            "Capítulo no válido."
        )

        tipo_colegiado = self.validate_required_field(
            'tipo_colegiado',
            validated_data.pop('tipo_colegiado', None),
            TipoColegiado,
            "Tipo de colegiado no válido."
        )

        consejo = self.validate_required_field(
            'consejo_departamental',
            validated_data.pop('consejo_departamental', None),
            ConsejoDepartamental,
            "Consejo departamental no válido."
        )

        colegiatura = self.validate_required_field(
            'colegiatura',
            validated_data.pop('colegiatura', None),
            Colegiatura,
            "Colegiatura no válida."
        )

        # Obtener estado activo
        try:
            activo = Activo.objects.get(id=2)
        except Activo.DoesNotExist:
            raise serializers.ValidationError(
                {"estado_activo": "El estado activo con id=2 no existe en la base de datos."}
            )

        # Crear o actualizar ingeniero
        ingeniero_data = {
            'tipo_documento': tipo_documento,
            'pais': pais,
            'apellido_paterno': validated_data.pop('apellido_paterno'),
            'apellido_materno': validated_data.pop('apellido_materno'),
            'nombres': validated_data.pop('nombres'),
            'numero_documento': validated_data.pop('numero_documento'),
            'correo': validated_data.pop('correo'),
            'celular': validated_data.pop('celular')
        }

        ingeniero, _ = Ingeniero.objects.update_or_create(
            numero_documento=ingeniero_data['numero_documento'],
            defaults=ingeniero_data
        )

        # Crear colegiado
        colegiado = Colegiado.objects.create(
            ingeniero=ingeniero,
            capitulo=capitulo,
            tipo_colegiado=tipo_colegiado,
            consejo_departamental=consejo,
            colegiatura=colegiatura,
            activo=activo
        )

        return colegiado

    def to_representation(self, instance):
        """Representación personalizada del objeto"""
        return {
            "id": instance.id,
            "estado_activo": instance.activo.id if instance.activo else None,
            "ingeniero": {
                "id": instance.ingeniero.id,
                "apellido_paterno": instance.ingeniero.apellido_paterno,
                "apellido_materno": instance.ingeniero.apellido_materno,
                "nombres": instance.ingeniero.nombres,
                "tipo_documento": {
                    "id": instance.ingeniero.tipo_documento.id,
                    "tipo": instance.ingeniero.tipo_documento.tipo
                } if instance.ingeniero.tipo_documento else None,
                "numero_documento": instance.ingeniero.numero_documento,
                "correo": instance.ingeniero.correo,
                "codigo_pais": {
                    "id": instance.ingeniero.pais.id,
                    "codigo": instance.ingeniero.pais.codigo,
                    "nombre": instance.ingeniero.pais.nombre
                } if instance.ingeniero.pais else None,
                "celular": instance.ingeniero.celular
            } if instance.ingeniero else None,
            "capitulo": {
                "id": instance.capitulo.id,
                "codigo": instance.capitulo.codigo,
                "nombre": instance.capitulo.nombre
            } if instance.capitulo else None,
            "consejo_departamental": {
                "id": instance.consejo_departamental.id,
                "departamento": instance.consejo_departamental.departamento
            } if instance.consejo_departamental else None,
            "colegiatura": {
                "id": instance.colegiatura.id,
                "nombre": instance.colegiatura.nombre
            } if instance.colegiatura else None,
            "tipo_colegiado": {
                "id": instance.tipo_colegiado.id,
                "descripcion": instance.tipo_colegiado.descripcion
            } if instance.tipo_colegiado else None,
        }

    def update(self, instance, validated_data):
        # Actualizar datos del ingeniero
        ingeniero_data = {}
        for field in ['tipo_documento', 'codigo_pais', 'apellido_paterno', 
                     'apellido_materno', 'nombres', 'numero_documento', 
                     'correo', 'celular']:
            if field in validated_data:
                if field == 'tipo_documento':
                    ingeniero_data['tipo_documento'] = self.validate_required_field(
                        'tipo_documento',
                        validated_data.pop('tipo_documento'),
                        TipoDocumento,
                        "Tipo de documento no válido."
                    )
                elif field == 'codigo_pais':
                    ingeniero_data['pais'] = self.validate_required_field(
                        'codigo_pais',
                        validated_data.pop('codigo_pais'),
                        Pais,
                        "País no válido."
                    )
                else:
                    ingeniero_data[field] = validated_data.pop(field)

        if ingeniero_data:
            for key, value in ingeniero_data.items():
                setattr(instance.ingeniero, key, value)
            instance.ingeniero.save()

        # Actualizar otros campos del colegiado
        for field in ['capitulo', 'tipo_colegiado', 'consejo_departamental', 'colegiatura']:
            if field in validated_data:
                model_class = {
                    'capitulo': Capitulo,
                    'tipo_colegiado': TipoColegiado,
                    'consejo_departamental': ConsejoDepartamental,
                    'colegiatura': Colegiatura
                }[field]
                
                value = self.validate_required_field(
                    field,
                    validated_data.pop(field),
                    model_class,
                    f"{field.replace('_', ' ').title()} no válido."
                )
                setattr(instance, field, value)

        instance.save()
        return instance
