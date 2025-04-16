from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# Create your models here.


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class MemberInfo(models.Model):
    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE, related_name='member_info')
    collegiate_type = models.ForeignKey(
        'CollegiateType', on_delete=models.CASCADE, related_name='member_info')
    dept_council = models.ForeignKey(
        'DepartmentalCouncil', on_delete=models.CASCADE, related_name='member_info')
    chapter = models.ForeignKey(
        'Chapter', on_delete=models.CASCADE, related_name='member_info')

    class Meta:
        db_table = 'member_info'


class Member(models.Model):
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='members')
    colligiate_code = models.CharField(max_length=20, unique=True)
    status = models.BooleanField(default=True)
    objects = SoftDeleteManager()

    def delete(self, using=None, keep_parents=False):
        self.status = False
        self.save()

    class Meta:
        db_table = 'members'


class Person(models.Model):
    paternal_surname = models.CharField(max_length=50)
    maternal_surname = models.CharField(max_length=50)
    names = models.CharField(max_length=50)
    document_type = models.ForeignKey(
        'DocumentType', on_delete=models.CASCADE, related_name='persons')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    doc_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        max_length=100, unique=True, null=True, blank=True)
    country = models.ForeignKey(
        'Country', on_delete=models.CASCADE, related_name='persons')
    cellphone = models.CharField(
        max_length=15, unique=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'persons'


class AcademicInfo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    diploma_date = models.DateField()
    institution = models.CharField(max_length=100)
    country = models.ForeignKey(
        'Country', on_delete=models.CASCADE, related_name='academic_info')
    professional_denomination = models.CharField(
        max_length=100, null=True, blank=True)
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='academic_info')

    class Meta:
        db_table = 'academic_info'


class DocumentType(models.Model):
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'documents_types'


class Country(models.Model):
    country_cod = models.CharField(max_length=10, unique=True)
    iso_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'countries'


# class Status(models.Model):
#     status_type = models.CharField(max_length=20, unique=True)

#     class Meta:
#         db_table = 'status'


class Chapter(models.Model):
    chapter_cod = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'chapters'


class CollegiateType(models.Model):
    colle_type = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'collegiate_types'


class DepartmentalCouncil(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'departmental_councils'


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