# Generated by Django 4.0.1 on 2022-06-22 21:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='age_restrictions',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(18)], verbose_name='возрастные ограничения'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='количество страниц'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)], verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='book',
            name='value_available',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='количество в наличии'),
        ),
        migrations.AlterField(
            model_name='book',
            name='weigh',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='вес'),
        ),
    ]
