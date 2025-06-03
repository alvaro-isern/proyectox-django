from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Person(models.Model):
    document_type = models.CharField(max_length=50, choices=[
        ('1', 'DNI'),
        ('2', 'CARNET DE EXTRANJERIA'),
        ('3', 'PASAPORTE'),
        ('4', 'CEDULA DIPLOMATICA DE IDENTIDAD'),
    ])
    doc_number = models.CharField(max_length=20, unique=True)
    names = models.CharField(max_length=100)
    paternal_surname = models.CharField(max_length=100)
    maternal_surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    civil_state = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('1', 'SOLTERO(A)'),
        ('2', 'CASADO(A)'),
        ('3', 'DIVORCIADO(A)'),
        ('4', 'VIUDO(A)'),
    ])
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='persons')
    is_active = models.BooleanField(default=True)
    objects = SoftDeleteManager()

    def delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    class Meta:
        db_table = 'persons'

class Contact(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='contacts_person')
    cellphone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_main = models.BooleanField(default=False, null=True, blank=True)
    use = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('1', 'PERSONAL'),
        ('2', 'LABORAL'),
        ('3', 'EMERGENCIA'),
    ])
    is_active = models.BooleanField(default=True)
    objects = SoftDeleteManager()

    def delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    class Meta:
        db_table = 'contacts_person'

class FamilyInformation(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='familyinformation_person')
    person_family = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='familyinformation_family')
    relationship = models.CharField(max_length=20, choices=[
        ('1', 'PADRE'),
        ('2', 'MADRE'),
        ('3', 'HERMANO(A)'),
        ('4', 'HIJO(A)'),
        ('5', 'CONYUGE'),
        ('6', 'OTRO'),
    ])
    is_dependent = models.BooleanField(default=False)
    is_emergency_contact = models.BooleanField(default=False)
    is_live = models.BooleanField(default=True)
    death_date = models.DateField(null=True, blank=True)

    cellphone = models.CharField(max_length=20)

    class Meta:
        db_table = 'family_information_person'

class JobExperience(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='job_experience_person')
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='job_experience_country', null=True,
                                blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    is_current_job = models.BooleanField(default=False, null=True, blank=True)
    job_situation = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('1', 'INDEPENDIENTE'),
        ('2', 'EMPLEADO'),
        ('3', 'DESEMPLEADO'),
    ])
    type_contract = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('1', 'NOMBRADO'),
        ('2', 'CONTRATADO'),
        ('3', 'LOCADOR'),
        ('4', 'CAS'),
        ('5', 'PART-TIME'),
        ('6', 'CONTRATO TEMPORAL'),
        ('7', 'CONTRATO POR SERVICIO'),
    ])

    class Meta:
        db_table = 'job_experience_person'

class AcademicTraining(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='academictraining_person')
    training_type = models.ForeignKey('TrainingType', on_delete=models.CASCADE, related_name='academictraining_type')
    institution = models.CharField(max_length=100)
    obtained_degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.ForeignKey(
        'Country', on_delete=models.CASCADE, related_name='academictraining_country')
    is_profetional_dregree = models.BooleanField(default=False)

    class Meta:
        db_table = 'trainings'

class TrainingType(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'training_types'

class Country(models.Model):
    country_cod = models.CharField(max_length=10, unique=True)
    iso_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    demonym = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'countries'

class Multinationality(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='multinationalities_person')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='multinationalities_country')

    class Meta:
        db_table = 'multinationalities'