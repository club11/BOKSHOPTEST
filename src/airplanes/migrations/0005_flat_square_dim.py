# Generated by Django 4.0.1 on 2022-01-22 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airplanes', '0004_squaredim'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='square_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='flats', to='airplanes.squaredim'),
            preserve_default=False,
        ),
    ]
