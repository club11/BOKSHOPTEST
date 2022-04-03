from django.contrib import admin
from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'tel',
    ]
admin.site.register(models.Profile, ProfileAdmin)
