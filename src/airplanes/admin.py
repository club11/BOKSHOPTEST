from django.contrib import admin
from django.forms import models

# Register your models here.
from . import models

class FlatAdmin(admin.ModelAdmin):
    list_display = ['pk',           # именно list_display
    'flat_number', 
    'created', 
    'updated', 
    'is_sold',
    'square',
    'square_dim']      

class SquareDimAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'dim',]      

admin.site.register(models.SquareDim,  SquareDimAdmin)
admin.site.register(models.Flat, FlatAdmin)
