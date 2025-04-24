from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# Create your models here.


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Engineer(models.Model):
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='engineers')
    colligiate_code = models.CharField(max_length=20, unique=True)
    status = models.BooleanField(default=True)
    training = models.ForeignKey('AcademicTraining', on_delete=models.CASCADE, related_name='engineers')
    registration_date = models.DateField()
    member_type = models.charField(max_length=20, choices=[
        (1, 'ORDINARIO'),
        (2, 'VITALICIO'),
    ])
    vitalicio_date = models.DateField(null=True, blank=True)
    departament_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='engineers')
    main_specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='engineers')
    objects = SoftDeleteManager()

    def delete(self, using=None, keep_parents=False):
        self.status = False
        self.save()

    class Meta:
        db_table = 'engineers'

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True, unique=True)
    creation_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'specialties'

class ChapterSpecialty(models.Model):
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='chapter_specialties')
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='chapter_specialties')
    is_main = models.BooleanField(default=False)
    incorporation_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'chapters_specialties'

class IngineerSpecialty(models.Model):
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE, related_name='engineer_specialties')
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='engineer_specialties')
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='engineer_specialties')
    registration_date = models.DateField(null=True, blank=True)
    is_main = models.BooleanField(default=False, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    class Meta:
        db_table = 'engineers_specialties'

class Person(models.Model):
    document_type = models.CharField(max_length=50, choices=[
        (1, 'DNI'),
        (2, 'CARNET DE EXTRANJERIA'),
        (3, 'PASAPORTE'),
        (4, 'CEDULA DIPLOMATICA DE IDENTIDAD'),
    ])
    doc_number = models.CharField(max_length=20, unique=True)
    names = models.CharField(max_length=100)
    paternal_surname = models.CharField(max_length=100)
    maternal_surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    civil_state = models.CharField(max_length=20, null=True, blank=True, choices=[
        (1, 'SOLTERO(A)'),
        (2, 'CASADO(A)'),
        (3, 'DIVORCIADO(A)'),
        (4, 'VIUDO(A)'),
    ])
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='persons')

    class Meta:
        db_table = 'persons'

class Contact(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='contacts')
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_main = models.BooleanField(default=False, null=True, blank=True)
    use = models.CharField(max_length=20, null=True, blank=True, choices=[
        (1, 'PERSONAL'),
        (2, 'LABORAL'),
        (3, 'EMERGENCIA'),
    ])

    class Meta:
        db_table = 'contacts'

class JobExperience(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='job_experiences')
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='job_experiences', null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    is_current_job = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'job_experiences'

class AcademicTraining(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='trainings')
    training_type = models.ForeignKey('TrainingType', on_delete=models.CASCADE, related_name='trainings')
    institution = models.CharField(max_length=100)
    obtained_degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.ForeignKey(
        'Country', on_delete=models.CASCADE, related_name='trainings')
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
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='multinationalities')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='multinationalities')

    class Meta:
        db_table = 'multinationalities'

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='provinces')

    class Meta:
        db_table = 'provinces'

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='districts')

    class Meta:
        db_table = 'districts'

class Chapter(models.Model):
    chapter_cod = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    departmental_council = models.ForeignKey('DepartmentalCouncil', on_delete=CASCADE, related_name='chapters')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'chapters'

class DepartmentalCouncil(models.Model):
    name = models.CharField(max_length=100, unique=True)
    headquarters = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='departmental_councils')
    address = models.CharField(max_length=100)
    telephone1 = models.CharField(max_length=20, null=True, blank=True)
    telephone2 = models.CharField(max_length=20, null=True, blank=True)
    telephone3 = models.CharField(max_length=20, null=True, blank=True)
    telephone4 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    zona = models.CharField(max_length=100, unique=True)
    creation_date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'departmental_councils'

class LocalCommittee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    provice = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='local_committees')
    address = models.CharField(max_length=100, null=True, blank=True)
    telephone1 = models.CharField(max_length=20, null=True, blank=True)
    telephone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    creation_date = models.DateField()
    departamental_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='local_committees')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'local_committees'

class InstitutionalArea(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'institutional_areas'

class DecentralizedHeadquarters(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='decentralized_headquarters')
    address = models.CharField(max_length=100, null=True, blank=True)
    telephone1 = models.CharField(max_length=20, null=True, blank=True)
    telephone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    creation_date = models.DateField()
    departamental_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='decentralized_headquarters')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'decentralized_headquarters'

# class DocumentType(models.Model):
#     type = models.CharField(max_length=50, unique=True)
#
#     class Meta:
#         db_table = 'documents_types'

# class Status(models.Model):
#     status_type = models.CharField(max_length=20, unique=True)

#     class Meta:
#         db_table = 'status'


# class CollegiateType(models.Model):
#     colle_type = models.CharField(max_length=100, unique=True)
#
#     class Meta:
#         db_table = 'collegiate_types'

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     user_type = models.ForeignKey(
#         'UserType', on_delete=models.CASCADE, related_name='users')

#     class Meta:
#         db_table = 'users'


# class UserType(AbstractUser):
#     type = models.CharField(max_length=100, unique=True)

#     class Meta:
#         db_table = 'user_types'

# class AuditLog(models.Model):
#     action = models.CharField(max_length=100)
#     model_name = models.CharField(max_length=100)
#     field_name = models.CharField(max_length=100)
#     object_id = models.PositiveIntegerField()
#     old_value = models.TextField(null=True, blank=True)
#     new_value = models.TextField(null=True, blank=True)
#     user = models.ForeignKey(
#         'User', on_delete=models.CASCADE, related_name='audit_logs')
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'audit_logs'
#         ordering = ['-timestamp']