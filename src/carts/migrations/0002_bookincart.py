# Generated by Django 4.0.1 on 2022-03-10 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_ratingstar_options'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='количество')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='цена')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books_in_cart', to='books.book', verbose_name='Книга')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='carts.cart', verbose_name='Корзина')),
            ],
        ),
    ]
