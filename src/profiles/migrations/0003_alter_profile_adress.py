# Generated by Django 4.0.1 on 2022-06-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_adress_profile_city_profile_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='adress',
            field=models.CharField(max_length=30, null=True, verbose_name='адрес'),
        ),
    ]
