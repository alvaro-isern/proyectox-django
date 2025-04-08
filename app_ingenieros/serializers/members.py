from rest_framework import serializers
from app_ingenieros.models import (
    Colegiado, Ingeniero, TipoDocumento, Pais, Activo,
    Colegiatura, Capitulo, TipoColegiado, ConsejoDepartamental
)

class MembersSerializer(serializers.ModelSerializer):
    apellido_paterno = serializers.CharField(write_only=True)
    apellido_materno = serializers.CharField(write_only=True)
    nombres = serializers.CharField(write_only=True)
    tipo_documento = serializers.CharField(write_only=True)
    numero_documento = serializers.CharField(write_only=True)
    correo = serializers.EmailField(write_only=True)
    codigo_pais = serializers.CharField(write_only=True)
    celular = serializers.CharField(allow_blank=True, write_only=True)
    colegiatura = serializers.IntegerField(write_only=True)
    tipo_colegiado = serializers.CharField(write_only=True)
    consejo_departamental = serializers.CharField(write_only=True)
    codigo_capitulo = serializers.CharField(write_only=True)
    capitulo = serializers.CharField(write_only=True)

    class Meta:
        model = Colegiado
        fields = [
            'id', 'apellido_paterno', 'apellido_materno', 'nombres',
            'tipo_documento', 'numero_documento', 'correo', 'codigo_pais', 'celular',
            'colegiatura', 'tipo_colegiado', 'consejo_departamental',
            'codigo_capitulo', 'capitulo'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # Crear o recuperar tipo de documento
        tipo_documento, _ = TipoDocumento.objects.get_or_create(tipo=validated_data.pop('tipo_documento'))

        # Crear o recuperar país
        pais, _ = Pais.objects.get_or_create(codigo=validated_data.pop('codigo_pais'), defaults={"nombre": "Desconocido"})

        # Crear o recuperar ingeniero
        ingeniero = Ingeniero.objects.create(
            apellido_paterno=validated_data.pop('apellido_paterno'),
            apellido_materno=validated_data.pop('apellido_materno'),
            nombres=validated_data.pop('nombres'),
            tipo_documento=tipo_documento,
            numero_documento=validated_data.pop('numero_documento'),
            correo=validated_data.pop('correo'),
            pais=pais,
            celular=validated_data.pop('celular')
        )

        # Crear o recuperar capitulo
        codigo_capitulo = validated_data.pop('codigo_capitulo')
        nombre_capitulo = validated_data.pop('capitulo')
        capitulo, _ = Capitulo.objects.get_or_create(codigo=codigo_capitulo, defaults={"nombre": nombre_capitulo})

        # Crear o recuperar tipo colegiado
        tipo_colegiado, _ = TipoColegiado.objects.get_or_create(descripcion=validated_data.pop('tipo_colegiado'))

        # Crear o recuperar consejo departamental
        consejo, _ = ConsejoDepartamental.objects.get_or_create(departamento=validated_data.pop('consejo_departamental'))

        # Crear o recuperar colegiatura
        numero_colegiatura = validated_data.pop('colegiatura')
        colegiatura, _ = Colegiatura.objects.get_or_create(nombre=str(numero_colegiatura))

        # Crear o recuperar estado activo por defecto
        activo, _ = Activo.objects.get_or_create(estado="Activo")

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
