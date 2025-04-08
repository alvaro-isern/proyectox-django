from rest_framework import serializers
from app_ingenieros.models import (
    Colegiado, Ingeniero, TipoDocumento, Pais, Activo,
    Colegiatura, Capitulo, TipoColegiado, ConsejoDepartamental
)


class MembersSerializer(serializers.ModelSerializer): 
    nombres = serializers.CharField(source='ingeniero.nombres')
    apellido_materno = serializers.CharField(source='ingeniero.apellido_materno')
    apellido_paterno = serializers.CharField(source='ingeniero.apellido_paterno')
    tipo_documento = serializers.IntegerField(source='ingeniero.tipo_documento.id')
    numero_documento = serializers.CharField(source='ingeniero.numero_documento')
    correo = serializers.EmailField(source='ingeniero.correo')
    codigo_pais = serializers.IntegerField(source='ingeniero.pais.id')
    celular = serializers.CharField(source='ingeniero.celular')
    estado_activo = serializers.IntegerField(source='activo.id')
    capitulo = serializers.IntegerField(source='capitulo.id')
    consejo_departamental = serializers.IntegerField(source='consejo_departamental.id')
    colegiatura = serializers.IntegerField(source='colegiatura.id')
    tipo_colegiado = serializers.IntegerField(source='tipo_colegiado.id')



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
        # Crear o recuperar tipo de documento
        tipo_documento, _ = TipoDocumento.objects.get(
            tipo=validated_data.pop('tipo_documento'))

        # Crear o recuperar país
        pais, _ = Pais.objects.get(codigo=validated_data.pop(
            'codigo_pais'), defaults={"nombre": "Desconocido"})

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
        capitulo, _ = Capitulo.objects.get_or_create(
            codigo=codigo_capitulo, defaults={"nombre": nombre_capitulo})

        # Crear o recuperar tipo colegiado
        tipo_colegiado, _ = TipoColegiado.objects.get_or_create(
            descripcion=validated_data.pop('tipo_colegiado'))

        # Crear o recuperar consejo departamental
        consejo, _ = ConsejoDepartamental.objects.get_or_create(
            departamento=validated_data.pop('consejo_departamental'))

        # Crear o recuperar colegiatura
        numero_colegiatura = validated_data.pop('colegiatura')
        colegiatura, _ = Colegiatura.objects.get_or_create(
            nombre=str(numero_colegiatura))

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

    def to_representation(self, instance):
        """Customize the serialized output."""
        representation = super().to_representation(instance)
        
        # Add related fields from Ingeniero model
        Ingeniero = instance.ingeniero
        if Ingeniero:
            representation['ingeniero'] = {
                'id': Ingeniero.id,
                'apellido_paterno': Ingeniero.apellido_paterno,
                'apellido_materno': Ingeniero.apellido_materno,
                'nombres': Ingeniero.nombres,
                'tipo_documento': {
                    'id': Ingeniero.tipo_documento.id,
                    'tipo': Ingeniero.tipo_documento.tipo
                },
                'numero_documento': Ingeniero.numero_documento,
                'correo': Ingeniero.correo,
                'codigo_pais': {
                    'id': Ingeniero.pais.id,
                    'codigo': Ingeniero.pais.codigo,
                    'nombre': Ingeniero.pais.nombre
                },
                'celular': Ingeniero.celular
            }
        else:
            representation['ingeniero'] = None
        

        # Add related fields from other models
        Capitulo = instance.capitulo
        if Capitulo:
            representation['capitulo'] = {
                'id': Capitulo.id,
                'codigo': Capitulo.codigo,
                'nombre': Capitulo.nombre
            }
        else:
            representation['capitulo'] = None

        TipoColegiado = instance.tipo_colegiado
        if TipoColegiado:
            representation['tipo_colegiado'] = {
                'id': TipoColegiado.id,
                'descripcion': TipoColegiado.descripcion
            }
        else:
            representation['tipo_colegiado'] = None
        
        ConsejoDepartamental = instance.consejo_departamental
        if ConsejoDepartamental:
            representation['consejo_departamental'] = {
                'id': ConsejoDepartamental.id,
                'departamento': ConsejoDepartamental.departamento
            }
        else:
            representation['consejo_departamental'] = None

        Colegiatura = instance.colegiatura
        if Colegiatura:
            representation['colegiatura'] = {
                'id': Colegiatura.id,
                'nombre': Colegiatura.nombre
            }
        else:
            representation['colegiatura'] = None

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
