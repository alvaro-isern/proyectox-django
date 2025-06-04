from django.db import models
from django.contrib.auth.models import User
from app_persons.models import Person, AcademicTraining, Country
# from django.utils import timezone
# Create your models here.


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Engineer(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='engineers')
    colligiate_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    registration_date = models.DateField()
    member_type = models.CharField(max_length=20, choices=[
        ('1', 'ORDINARIO'),
        ('2', 'VITALICIO'),
    ])
    vitalicio_date = models.DateField(null=True, blank=True)
    departament_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='engineers')
    objects = SoftDeleteManager()

    def delete(self):
        self.status = False
        self.save()

    def restore(self):
        self.status = True
        self.save()

    class Meta:
        db_table = 'engineers_departmental'

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True, unique=True)
    creation_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'specialties_departmental'

class ChapterSpecialty(models.Model):
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='chapter_specialty_departmental')
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='chapter_specialty_departmental')
    incorporation_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'chapter_specialty_departmental'

class EngineerSpecialty(models.Model):
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE, related_name='engineer_specialty_departmental')
    specialty_charter = models.ForeignKey('ChapterSpecialty', on_delete=models.CASCADE, related_name='engineer_specialty_departmental')
    registration_date = models.DateField(null=True, blank=True)
    is_main = models.BooleanField(default=False, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    class Meta:
        db_table = 'engineer_specialty_departmental'

class EngineerTraining(models.Model):
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE, related_name='engineer_training_departmental')
    training = models.ForeignKey(AcademicTraining, on_delete=models.CASCADE, related_name='engineer_training_departmental')
    is_main = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'engineer_training_departmental'

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='provinces')

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
    departmental_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='chapters')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'chapters_departmental'

class DepartmentalCouncil(models.Model):
    name = models.CharField(max_length=100, unique=True)
    headquarters = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='departmental_councils')
    institutional_area = models.ForeignKey('InstitutionalArea', on_delete=models.CASCADE, related_name='departmental_councils')
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'departmental_councils'

class DepartmentalCouncilPhone(models.Model):
    departamental_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='phones')
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_main = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'departmental_council_phones'

class LocalCommittee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    departamental_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='local_committees_departmental')
    address = models.CharField(max_length=100, null=True, blank=True)
    telephone1 = models.CharField(max_length=20, null=True, blank=True)
    telephone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    creation_date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'local_committees_departmental'

class InstitutionalArea(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'institutional_areas_departmental'

class DecentralizedHeadquarters(models.Model):
    name = models.CharField(max_length=100, unique=True)
    departamental_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='decentralized_headquarters_departmental')
    address = models.CharField(max_length=100, null=True, blank=True)
    telephone1 = models.CharField(max_length=20, null=True, blank=True)
    telephone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    creation_date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'decentralized_headquarters_departmental'

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