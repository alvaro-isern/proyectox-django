from django.db import models
from django.utils import timezone
# Create your models here.
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True

class Member(BaseModel):
    colligiate_code = models.CharField(max_length=20, unique=True)
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE, related_name='members')
    collegiate_type = models.ForeignKey('CollegiateType', on_delete=models.CASCADE, related_name='members')
    dept_council = models.ForeignKey('DepartmentalCouncil', on_delete=models.CASCADE, related_name='members')
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='members')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='members')

    def delete(self, using=None, keep_parents=False):
        self.status = Status.objects.get(id=1)
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'members'

class Engineer(BaseModel):
    paternal_surname = models.CharField(max_length=50)
    maternal_surname = models.CharField(max_length=50)
    names = models.CharField(max_length=50)
    doc_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, related_name='engineers')
    doc_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='engineers')
    cellphone = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'engineers'


class DocumentType(models.Model):
    doc_type = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'documents_types'


class Country(models.Model):
    country_cod = models.CharField(max_length=10, unique=True)
    iso_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'countries'


class Status(models.Model):
    status_type = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'status'


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