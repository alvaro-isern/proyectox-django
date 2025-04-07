from django.db import models
from app_ingenieros.models import Colegiado 

class MetodoPago(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Método de Pago",
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'metodos_pago'
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"


class Cuota(models.Model):
    colegiado = models.ForeignKey(
        Colegiado,
        on_delete=models.CASCADE,
        related_name='cuotas',
        verbose_name="Colegiado",
    )
    fecha_vencimiento = models.DateField(
        verbose_name="Fecha de Vencimiento",
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto",
    )
    estado_cuota = models.ForeignKey(
        'EstadoCuota',
        on_delete=models.CASCADE,
        related_name='cuotas',
        verbose_name="Estado de Cuota",
    )

    def __str__(self):
        return f"Cuota de {self.colegiado} - Vence: {self.fecha_vencimiento}"

    class Meta:
        db_table = 'cuotas'
        ordering = ['fecha_vencimiento']
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"


class Pagos(models.Model):
    colegiado = models.ForeignKey(
        Colegiado,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Colegiado",
    )
    fecha_pago = models.DateField(
        verbose_name="Fecha de Pago",
    )
    monto_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto del Pago",
    )
    metodo_pago = models.ForeignKey(
        'MetodoPago',
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Método de Pago",
    )
    cuota = models.ForeignKey(
        'Cuota',
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Cuota",
    )

    def __str__(self):
        return f"Pago de {self.colegiado} - {self.fecha_pago} - {self.monto_pago}"

    class Meta:
        db_table = 'pagos'
        ordering = ['-fecha_pago']
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

class EstadoCuota(models.Model):
    estado = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Estado de Cuota",
    )

    def __str__(self):
        return self.estado

    class Meta:
        db_table = 'estado_cuota'
        verbose_name = "Estado de Cuota"
        verbose_name_plural = "Estados de Cuota"