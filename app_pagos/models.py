from django.db import models
from app_ingenieros.models import Member


class PaymentMethod(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Método de Pago",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'payment_methods'
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"


class PaymentFee(models.Model):
    due_date = models.DateField(
        verbose_name="Due Date",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
    )
    quota_status = models.ForeignKey(
        'QuotaStatus',
        on_delete=models.CASCADE,
        related_name='payment_fees',
        verbose_name="Quota Status",
    )

    def __str__(self):
        return f"Member: {self.member} - Expiration Date: {self.due_date}"

    class Meta:
        db_table = 'payment_fees'
        ordering = ['due_date']
        verbose_name = "Payment Fee"
        verbose_name_plural = "Payment Fees"


class Payment(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Member",
    )
    payment_date = models.DateField(
        verbose_name="Payment Date",
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Payment Amount",
    )
    payment_method = models.ForeignKey(
        'PaymentMethod',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Payment Method",
    )
    payment_fee = models.ForeignKey(
        'PaymentFee',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Payment Fee",
    )

    def __str__(self):
        return f"Payment: {self.member} - {self.payment_date} - {self.payment_amount}"

    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class QuotaStatus(models.Model):
    quota_status = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Quota Status",
    )

    def __str__(self):
        return self.quota_status

    class Meta:
        db_table = 'quota_status'
        verbose_name = "Quota Status"
