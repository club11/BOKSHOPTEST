# Generated by Django 4.0.1 on 2022-04-28 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_contact_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='contact_info',
            field=models.TextField(verbose_name='контактная информация'),
        ),
    ]
