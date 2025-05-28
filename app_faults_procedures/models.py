from django.db import models
from app_engineers.models import Engineer, DepartmentalCouncil
from app_events.models import Period

# Create your models here.
class Sanction(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='sanctions', verbose_name="Case")
    sanction_type = models.CharField(max_length=50, verbose_name="Sanction Type", choices=[
        (1, 'FALTA ÉTICA'),
        (2, 'FALTA CONTRA LA INSTITUCION'),
        (3, 'FALTA CONTRA EL ESTUTO'),
        (4, 'FATA A LOS REGLAMENTOS'),
        (5, 'FALTA CONTRA RESOLUCIONES'),
        (6, 'OTRO'),
    ])
    start_date = models.DateField(
        verbose_name="Start Date",
    )
    end_date = models.DateField(
        verbose_name="End Date",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        null=True,
        blank=True,
    )
    resolution_number = models.CharField(max_length=50, verbose_name="Resolution Number", null=True, blank=True)
    resolution_date = models.DateField(
        verbose_name="Resolution Date",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'sanctions'
        verbose_name = "Sanction"
        verbose_name_plural = "Sanctions"

class Case(models.Model):
    court = models.ForeignKey('Court', on_delete=models.CASCADE, related_name='cases', verbose_name="Court")
    case_code = models.CharField(max_length=50, verbose_name="Case Number", null=True, blank=True)
    start_date = models.DateField(
        verbose_name="Start Date",
    )
    end_date = models.DateField(
        verbose_name="End Date",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    engineer_involved = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='cases', verbose_name="Engineer Involved")
    complainant = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='complaints', verbose_name="Complainant")
    instance = models.CharField(max_length=50, verbose_name="Instance", choices=[
        (1, 'PRIMERA INSTANCIA'),
        (2, 'SEGUNDA INSTANCIA'),
        (3, 'TERCERA INSTANCIA'),
        (4, 'CUARTA INSTANCIA'),
        (5, 'QUINTA INSTANCIA'),
    ])

    class Meta:
        db_table = 'cases'
        verbose_name = "Case"
        verbose_name_plural = "Cases"

class Court(models.Model):
    departament_council = models.ForeignKey(DepartmentalCouncil, on_delete=models.CASCADE, related_name='courts', verbose_name="Departmental Council")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='courts', verbose_name="Period")
    start_date = models.DateField(
        verbose_name="Start Date",
    )
    end_date = models.DateField(
        verbose_name="End Date",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, verbose_name="Status", choices=[
        (1, 'ACTIVO'),
        (2, 'INACTIVO'),
    ], default=1)

    class Meta:
        db_table = 'courts'
        verbose_name = "Court"
        verbose_name_plural = "Courts"

class TribunalMember(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='tribunal_members', verbose_name="Court")
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='tribunal_members', verbose_name="Engineer")
    position = models.CharField(max_length=50, verbose_name="Position", choices=[
        (1, 'PRESIDENTE'),
        (2, 'SECRETARIO'),
        (3, 'VOCAL'),
    ], null=True, blank=True)
    start_date = models.DateField(
        verbose_name="Start Date",
    )
    end_date = models.DateField(
        verbose_name="End Date",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'tribunal_members'
        verbose_name = "Tribunal Member"
        verbose_name_plural = "Tribunal Members"