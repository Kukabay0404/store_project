from django.db import models
from users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) #max_digits= макс кол-во цифр до запятой
    #decimal_places= кол-во цифр после запятой
    quantity = models.PositiveIntegerField(default=0) #PositiveIntegerField(default=0) = int значение больше 0
    image = models.ImageField(upload_to='products_images') #ImageField- работа с изображениями, upload_to=('название папки') - загружает изображения в определенную папку
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    #ForeignKey - связывает две таблицы, to=ProductCategory - c какой таблицей идет связывание, on_delete= - определяет что делать при удалении,
    #on_delete=models.CASCADE - при удалении категории удалятся все данные вместе с ним
    #on_delete=models.PROTECT - категория не будет удалена пока все данные в нем не будут удалены
    #on_delete=models.SET_DEFAULT, default() - указывается дефолтное значение#

    def __str__(self):
        return f'Продукт {self.name} | категория {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
