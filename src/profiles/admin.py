from django.contrib import admin
from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'tel',
        'email',
        'first_name',
        'last_name',
        'country',
        'city',
        'index',
        'adress',

    ]
admin.site.register(models.Profile, ProfileAdmin)

