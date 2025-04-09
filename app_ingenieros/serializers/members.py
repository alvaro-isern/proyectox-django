from rest_framework import serializers
from app_ingenieros.models import (
    Colegiado, Ingeniero, TipoDocumento, Pais, Activo,
    Colegiatura, Capitulo, TipoColegiado, ConsejoDepartamental
)


class MembersSerializer(serializers.ModelSerializer):
    nombres = serializers.CharField(source='ingeniero.nombres')
    apellido_materno = serializers.CharField(
        source='ingeniero.apellido_materno')
    apellido_paterno = serializers.CharField(
        source='ingeniero.apellido_paterno')
    tipo_documento = serializers.IntegerField()
    numero_documento = serializers.CharField(
        source='ingeniero.numero_documento')
    correo = serializers.EmailField(source='ingeniero.correo')
    codigo_pais = serializers.IntegerField()
    celular = serializers.CharField(source='ingeniero.celular')
    estado_activo = serializers.IntegerField()
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
        read_only_fields = ['id', 'estado_activo']
        # read_only_fields = ['documento']

    def create(self, validated_data):
        # Validar y obtener tipo de documento
        tipo_documento_id = validated_data.pop('tipo_documento', None)
        if not tipo_documento_id:
            raise serializers.ValidationError(
                {"tipo_documento": "Este campo es obligatorio."}
            )
        try:
            tipo_documento, _ = TipoDocumento.objects.get_or_create(
                id=tipo_documento_id)
        except TipoDocumento.DoesNotExist:
            raise serializers.ValidationError(
                {"tipo_documento": "Tipo de documento no válido."}
            )

        # Validar y obtener país
        codigo_pais_id = validated_data.pop('codigo_pais', None)
        if not codigo_pais_id:
            raise serializers.ValidationError(
                {"codigo_pais": "Este campo es obligatorio."}
            )
        try:
            pais, _ = Pais.objects.get_or_create(id=codigo_pais_id)
        except Pais.DoesNotExist:
            raise serializers.ValidationError(
                {"codigo_pais": "País no válido."}
            )

        # Crear o recuperar ingeniero
        ingeniero, _ = Ingeniero.objects.get_or_create(
            tipo_documento=tipo_documento,
            pais=pais,
            apellido_paterno=validated_data.pop('apellido_paterno'),
            apellido_materno=validated_data.pop('apellido_materno'),
            nombres=validated_data.pop('nombres'),
            numero_documento=validated_data.pop('numero_documento'),
            correo=validated_data.pop('correo'),
            celular=validated_data.pop('celular')
        )

        # Crear o recuperar capitulo
        capitulo_id = validated_data.pop('capitulo', None)
        if not capitulo_id:
            raise serializers.ValidationError(
                {"capitulo": "Este campo es obligatorio."}
            )
        capitulo, _ = Capitulo.objects.get_or_create(id=capitulo_id)
        if not capitulo:
            raise serializers.ValidationError(
                {"capitulo": "Capítulo no válido."}
            )

        # Crear o recuperar tipo colegiado
        tipo_colegiado_id = validated_data.pop('tipo_colegiado', None)
        if not tipo_colegiado_id:
            raise serializers.ValidationError(
                {"tipo_colegiado": "Este campo es obligatorio."}
            )
        tipo_colegiado, _ = TipoColegiado.objects.get_or_create(
            id=tipo_colegiado_id
        )

        # Crear o recuperar consejo departamental
        consejo_departamental_id = validated_data.pop(
            'consejo_departamental', None
        )
        if not consejo_departamental_id:
            raise serializers.ValidationError(
                {"consejo_departamental": "Este campo es obligatorio."}
            )
        consejo, _ = ConsejoDepartamental.objects.get_or_create(
            id=consejo_departamental_id
        )

        # Crear o recuperar colegiatura
        colegiatura_id = validated_data.pop('colegiatura', None)
        if not colegiatura_id:
            raise serializers.ValidationError(
                {"colegiatura": "Este campo es obligatorio."}
            )
        try:
            colegiatura, _ = Colegiatura.objects.get_or_create(
                id=colegiatura_id)
        except Colegiatura.DoesNotExist:
            raise serializers.ValidationError(
                {"colegiatura": "Colegiatura no válida."}
            )

        # Crear o recuperar estado activo por defecto
        activo, _ = Activo.objects.get_or_create(
            id=validated_data.pop('estado_activo', None))

        # Finalmente, crear Colegiado
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
        """Customize the serialized output to avoid duplication."""
        representation = {
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
        return representation

    def update(self, instance, validated_data):
        # Actualizar o recuperar tipo de documento
        if 'tipo_documento' in validated_data:
            tipo_documento, _ = TipoDocumento.objects.get_or_create(
                tipo=validated_data.pop('tipo_documento'))
            instance.ingeniero.tipo_documento = tipo_documento

        # Actualizar o recuperar país
        if 'codigo_pais' in validated_data:
            pais, _ = Pais.objects.get_or_create(codigo=validated_data.pop(
                'codigo_pais'), defaults={"nombre": "Desconocido"})
            instance.ingeniero.pais = pais

        # Actualizar datos del ingeniero
        ingeniero_fields = ['apellido_paterno', 'apellido_materno',
                            'nombres', 'numero_documento', 'correo', 'celular']
        for field in ingeniero_fields:
            if field in validated_data:
                setattr(instance.ingeniero, field, validated_data.pop(field))
        instance.ingeniero.save()

        # Actualizar o recuperar capitulo
        if 'codigo_capitulo' in validated_data and 'capitulo' in validated_data:
            codigo_capitulo = validated_data.pop('codigo_capitulo')
            nombre_capitulo = validated_data.pop('capitulo')
            capitulo, _ = Capitulo.objects.get_or_create(
                codigo=codigo_capitulo, defaults={"nombre": nombre_capitulo})
            instance.capitulo = capitulo

        # Actualizar o recuperar tipo colegiado
        if 'tipo_colegiado' in validated_data:
            tipo_colegiado, _ = TipoColegiado.objects.get_or_create(
                descripcion=validated_data.pop('tipo_colegiado'))
            instance.tipo_colegiado = tipo_colegiado

        # Actualizar o recuperar consejo departamental
        if 'consejo_departamental' in validated_data:
            consejo, _ = ConsejoDepartamental.objects.get_or_create(
                departamento=validated_data.pop('consejo_departamental'))
            instance.consejo_departamental = consejo

        # Actualizar o recuperar colegiatura
        if 'colegiatura' in validated_data:
            numero_colegiatura = validated_data.pop('colegiatura')
            colegiatura, _ = Colegiatura.objects.get_or_create(
                nombre=str(numero_colegiatura))
            instance.colegiatura = colegiatura

        # Guardar cambios en el objeto Colegiado
        instance.save()

        return instance
