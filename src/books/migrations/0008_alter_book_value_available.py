# Generated by Django 4.0.1 on 2022-06-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_book_age_restrictions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='value_available',
            field=models.IntegerField(blank=True, verbose_name='количество в наличии'),
        ),
    ]
