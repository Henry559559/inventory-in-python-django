from django.db import models
from autoslug import AutoSlugField

class Bill(models.Model):
    slug = AutoSlugField(unique=True, populate_from='date')
    date = models.DateTimeField(auto_now_add=True, verbose_name=('Date (eg: 2022/11/22)'))
    institution_name = models.CharField(max_length=30, blank=False, null=False, verbose_name=('Nombre de la institución'))
    phone_number = models.IntegerField(blank=True, null=True, verbose_name=('Número de teléfono'))
    email = models.EmailField(null=True, blank=True, verbose_name=('Correo electrónico'))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=('Dirección'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=('Descripción'))
    payment_details = models.CharField(max_length=255, blank=False, null=False, verbose_name=('Detalles de pago'))
    amount = models.FloatField(verbose_name=('Monto total adeudado (Pesos)'))
    status = models.BooleanField(default=False, verbose_name=('Pagado'))

    def __str__(self):
        return self.institution_name
