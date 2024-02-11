from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return self.category.name
    

class Cart(models.Model):
    pass

    class Meta:
        verbose_name = 'Carrito de compra'
        verbose_name_plural = 'Carritos de compra'
    def __str__(self):
        return f'Carrito de compra {self.id}'    

    @property
    def total_items(self):
        return self.items.count()
        
    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Carrito de compra'
        verbose_name_plural = 'Carritos de compra'


    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        return self.product.price * self.quantity
