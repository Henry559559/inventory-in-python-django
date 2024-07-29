# tutorial/tables.py
import django_tables2 as tables
from .models import Item, Delivery, Category
from django.shortcuts import render
from accounts.models import Vendor
class ItemTable(tables.Table):
    class Meta:
        model = Item
        template_name = "django_tables2/semantic.html"
        fields = ('id', 'name','category', 'quantity', 'selling_price', 'expiring_date', 'vendor')
        order_by_field = 'sort'

class DeliveryTable(tables.Table):
    class Meta:
        model = Delivery
        fields = ('id', 'item', 'customer_name', 'phone_number', 'location', 'date','is_delivered')

class CategoryTable(tables.Table):
    class Meta:
        model = Category
        fields = ('id','name')
        
class VendorTable(tables.Table):
        class Meta:
            model = Vendor
            fields = ('id','name','phone_number', 'address')