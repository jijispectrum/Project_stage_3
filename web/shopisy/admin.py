from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin


from django.contrib import admin
from .models import Product,CartItem

admin.site.register(Product)

admin.site.register(CartItem)
