# Generated by Django 4.0.1 on 2022-06-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_age_restrictions_alter_book_pages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='age_restrictions',
            field=models.CharField(blank=True, max_length=20, verbose_name='возрастные ограничения'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(blank=True, verbose_name='количество страниц'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='book',
            name='value_available',
            field=models.IntegerField(blank=True, verbose_name='количество в наличии'),
        ),
        migrations.AlterField(
            model_name='book',
            name='weigh',
            field=models.IntegerField(blank=True, verbose_name='вес'),
        ),
    ]
