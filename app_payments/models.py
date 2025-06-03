from django.db import models
from app_engineers.models import Engineer, DepartmentalCouncil
from app_events.models import EventInscription
from app_faults_procedures.models import Sanction


class PaymentFee(models.Model):
    name = models.CharField(max_length=50, verbose_name="Payment Fee Name", null=True, blank=True)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
    )
    period = models.CharField(max_length=20, verbose_name="Period")
    ambit = models.CharField(max_length=20, verbose_name="Ambit")
    quota_status = models.CharField(
        max_length=20,
        verbose_name="Quota Status",
        choices=[
            ('1', 'PAGADO'),
            ('2', 'VENCIDO'),
            ('3', 'PENDIENTE'),
            ('4', 'CANCELADO'),
        ],
        default=3,
    )
    due_date = models.DateField(
        verbose_name="Due Date",
    )

    class Meta:
        db_table = 'payment_fees'
        verbose_name = "Payment Fee"
        verbose_name_plural = "Payment Fees"

class Payment(models.Model):
    payment_concept = models.ForeignKey(
        'PaymentConcept',
        on_delete=models.CASCADE,
        related_name='%(class)s_payments',
        verbose_name="Payment Concept",
    )
    payment_date = models.DateField(
        verbose_name="Payment Date",
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Payment Amount",
    )
    payment_method = models.CharField(
        max_length= 50, choices=[
            ('1', 'EFECTIVO'),
            ('2', 'TARJETA DE CREDITO/DEBITO'),
            ('3', 'YAPE/PLIN')
        ]
    )
    operation_number = models.CharField(max_length=50, verbose_name="Operation Number", null=True, blank=True)
    status = models.CharField(max_length=20, verbose_name="Status", choices=[
        ('1', 'PAGADO'),
        ('2', 'VENCIDO'),
        ('3', 'PENDIENTE'),
        ('4', 'CANCELADO'),
    ], default=3)
    departament_council = models.ForeignKey(
        DepartmentalCouncil,
        on_delete=models.CASCADE,
        related_name='%(class)s_payments',
        verbose_name="Departmental Council",
    )

    class Meta:
        db_table = 'payments'
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        abstract = True

class PaymentConcept(models.Model):
    code = models.CharField(max_length=50, verbose_name="Payment Concept Code", unique=True)
    name = models.CharField(max_length=50, verbose_name="Payment Concept Name")
    description = models.TextField(verbose_name="Description", null=True, blank=True)

    class Meta:
        db_table = 'payment_concepts'
        verbose_name = "Payment Concept"
        verbose_name_plural = "Payment Concepts"

class EventPayment(Payment):
    event_inscription = models.ForeignKey(
        EventInscription,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Event Inscription",
    )

    class Meta:
        db_table = 'event_payments'
        verbose_name = "Event Payment"
        verbose_name_plural = "Event Payments"

class SanctionPayment(Payment):
    sanction = models.ForeignKey(
        Sanction,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Sanction",
    )

    class Meta:
        db_table = 'sanction_payments'
        verbose_name = "Sanction Payment"
        verbose_name_plural = "Sanction Payments"

class QuotaPayment(Payment):
    engineer = models.ForeignKey(
        Engineer,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Engineer",
    )
    payment_fee = models.ForeignKey(
        "PaymentFee",
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Payment Fee",
    )

    class Meta:
        db_table = 'quota_payments'
        verbose_name = "Quota Payment"
        verbose_name_plural = "Quota Payments"


# class QuotaStatus(models.Model):
#     quota_status = models.CharField(
#         max_length=20,
#         unique=True,
#         verbose_name="Quota Status",
#     )
#
#     def __str__(self):
#         return self.quota_status
#
#     class Meta:
#         db_table = 'quota_status'
#         verbose_name = "Quota Status"


# class PaymentMethod(models.Model):
#     name = models.CharField(
#         max_length=50,
#         unique=True,
#         verbose_name="Método de Pago",
#     )
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'payment_methods'
#         verbose_name = "Payment Method"
#         verbose_name_plural = "Payment Methods"