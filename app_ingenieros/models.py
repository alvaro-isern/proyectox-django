from django.db import models

# Create your models here.
class Colegiado(models.Model):
    ingeniero = models.ForeignKey('Ingeniero', on_delete=models.CASCADE, related_name='colegiados')
    colegiatura = models.ForeignKey('Colegiatura', on_delete=models.CASCADE, related_name='colegiados')
    tipo_colegiado = models.ForeignKey('TipoColegiado', on_delete=models.CASCADE, related_name='colegiados')
    consejo_departamental = models.ForeignKey('ConsejoDepartamental', on_delete=models.CASCADE, related_name='colegiados')
    capitulo = models.ForeignKey('Capitulo', on_delete=models.CASCADE, related_name='colegiados')
    activo = models.ForeignKey('Activo', on_delete=models.CASCADE, related_name='colegiados')

    class Meta:
        db_table = 'colegiados'


class Ingeniero(models.Model):
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    tipo_documento = models.ForeignKey('TipoDocumento', on_delete=models.CASCADE, related_name='ingenieros')
    numero_documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=100, unique=True)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE, related_name='ingenieros')
    celular = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'ingenieros'


class TipoDocumento(models.Model):
    tipo = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tipo_documento'


class Pais(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'pais'


class Activo(models.Model):
    estado = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'activo'


class Colegiatura(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'colegiaturas'


class Capitulo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'capitulos'


class TipoColegiado(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tipo_colegiado'


class ConsejoDepartamental(models.Model):
    departamento = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'consejo_departamental'