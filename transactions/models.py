from django.db import models
from store.models import Item
from accounts.models import Profile, Vendor
from django_extensions.db.fields import AutoSlugField

# Create your models here.

PAYMENT_CHOICES = [
    ('VISA', 'VISA'),
    ('CS', 'EFECTIVO'),
    ('PS', 'PSE'),
    ('BK', 'BANCO')
]

DELIVERY_CHOICES = [
    ('P', 'Pendiente'),
    ('S', 'Entregado')
]

class Sale(models.Model):
    slug = AutoSlugField(unique=True , populate_from='customer_name')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True, verbose_name=('Producto'))
    customer_name = models.CharField(max_length=20, null=True, blank=True, verbose_name=('Nombre Del Cliente'))
    transaction_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    quantity = models.FloatField(default=0.00, blank=False, null=False, verbose_name=('Cantidad'))
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=20, blank='True', null=True, verbose_name=('Forma De Pago'))
    price = models.FloatField(default=0.00, blank=False, null=False, verbose_name=('Valor'))
    total_value = models.FloatField(blank=True, null=True)
    amount_received = models.FloatField(default=False, blank=False, null=False,  verbose_name=('Cantidad Recibida'))
    balance = models.FloatField(default=False, blank=False, null=False)
    profile = models.ForeignKey(Profile, verbose_name=('Served by'), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        amt_received = self.amount_received
        price = self.price
        quantity = self.quantity
        self.total_value = price * quantity
        self.balance = amt_received - self.total_value
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.item.name)

class Purchase(models.Model):
    slug = AutoSlugField(unique=True , populate_from='vendor')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=('Producto'))
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name=('Descripcion'))
    vendor = models.ForeignKey(Vendor, related_name='vendor', on_delete=models.CASCADE, blank=False, null=False, verbose_name=('Proveedor'))
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=('Fecha de entrega'))
    quantity = models.FloatField(default=0.00, blank=False, null=False, verbose_name=('Cantidad'))
    delivery_status = models.CharField(choices=DELIVERY_CHOICES, max_length=3, default='P', blank=False, null=False, verbose_name=('Estado de la entrega'))
    price = models.FloatField(default=0.00, blank=False, null=False, verbose_name=('Precio por artículo (Pesos)*'))
    total_value = models.FloatField()

    def save(self, *args, **kwargs):
        quantity = self.quantity
        price = self.price
        self.total_value = price * quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ["order_date"]
