"""
Module: models.py

Contains Django models for handling categories, items, and deliveries.

This module defines the following classes:
- Category: Represents a category for items.
- Item: Represents an item in the inventory.
- Delivery: Represents a delivery of an item to a customer.

Each class provides specific fields and methods for handling related data.
"""
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Vendor

class Category(models.Model):
    """
    Represents a category for items.
    """
    slug = AutoSlugField(unique=True , populate_from='name')
    name = models.CharField(max_length=50)

    def __str__(self):
        """
        String representation of the category.
        """
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Categories'

class Item(models.Model):
    """
    Represents an item in the inventory.
    """
    slug = AutoSlugField(unique=True , populate_from='name')
    name = models.CharField(max_length=50, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.00)
    selling_price = models.FloatField(default=0)
    expiring_date = models.DateTimeField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String representation of the item.
        """
        return f"{self.name} - Category: {self.category}, Quantity: {self.quantity}"

    def get_absolute_url(self):
        """
        Returns the absolute URL for an item detail view.
        """
        return reverse('item-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Items"

class Delivery(models.Model):
    """
    Represents a delivery of an item to a customer.
    """
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Producto')
    customer_name = models.CharField(blank=True, null=True, max_length=30, verbose_name='Nombre Del Cliente')
    phone_number = PhoneNumberField(null=True, blank=True, verbose_name='Numero De Telefono')
    location = models.CharField(blank=True, null=True, max_length=20, verbose_name='Ciudad O Pais De Entrega')
    date = models.DateTimeField(null=False, blank=False, verbose_name='Fecha De Entrega')
    is_delivered = models.BooleanField(default=False, verbose_name='Entregado')

    def __str__(self):
        """
        String representation of the delivery.
        """
        return (
            f"Delivery of {self.item} to {self.customer_name} "
            f"at {self.location} on {self.date}"
        )
