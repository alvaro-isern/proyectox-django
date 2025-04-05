from django.db import models

# Create your models here.
class Colegiados(models.Model):
    ingenieros_id = models.IntegerField()
    colegiatura_id = models.IntegerField()
    tipo_colegio_id = models.IntegerField()
    consejo_departamental_id = models.IntegerField()
    capitulo_id = models.IntegerField()
    activo_id = models.IntegerField()

    class Meta:
        db_table = 'colegiados'

class Ingenieros(models.Model):
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    tipodocumento_id = models.IntegerField()
    numero_documento = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    pais_id = models.IntegerField()
    celular = models.CharField(max_length=50)

    class Meta:
        db_table = 'ingenieros'


class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo_documento'

class Pais(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_pais = models.CharField(max_length=50)
    nombre_pais = models.CharField(max_length=50)

    class Meta:
        db_table = 'pais'

class Activo(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'activo'

class Colegiaturas(models.Model):
    nombre_colegiatura = models.CharField(max_length=50)

    class Meta:
        db_table = 'colegiaturas'

class Capitulos(models.Model):
    codigo_capitulo = models.CharField(max_length=50)
    nombre_capitulo = models.CharField(max_length=50)

    class Meta:
        db_table = 'capitulos'