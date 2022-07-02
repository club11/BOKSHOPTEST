from django.db import models
from django.contrib.auth import get_user_model
from books import models as books_models
from django.core.validators import MaxValueValidator

User = get_user_model()
class Cart(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name="Корзина",
        related_name='carts',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def cart_total_price(self):                           #ВАУ
        cart_total_price = 0                    
        goods = self.cart.all()                             #получаем все товары из модели BookInCart путем прохода по связи related_name='cart', all() все объекты в созданную переменную goods
        for good in goods:
            cart_total_price += good.total_price()          # а тут ваще бомба: через переменную-счетчик good обращаемся к функции total_price() модели BookInCart и суммируем все прайсы
        return cart_total_price

class BookInCart(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name='Корзина',
        related_name='cart',                    # имя, по которому можно обратиться к корзине (типо товары (в корзине)) типо как goods  - товары. обращение выйдет cart.cart.all()
        on_delete=models.CASCADE,        
    )
    book = models.ForeignKey(
        'books.Book',                           # ЛЕНИВЫЙ СПОСОБ ИМПОРТИРОВАНИЯ МОДЕЛИ
        verbose_name='Книга',
        related_name='books_in_cart',
        on_delete=models.PROTECT,
    )
    def max_quantity(self):                                                         #########
        max_quantity = self.book.value_available                                    #########
        return max_quantity                                                         #########

    quantity = models.IntegerField(
        verbose_name='количество',
        default=1,
        validators=[MaxValueValidator(max_quantity)]                                #########
    )
    unit_price = models.DecimalField(
        verbose_name='цена',      
        max_digits=6,
        decimal_places=2,
    )

    #@property                    # чтоб обращаться как к свойству а не как к методу
    def total_price(self):
        total_price = self.quantity * self.unit_price
        return total_price


