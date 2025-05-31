from django.db import models
from django.contrib.auth.models import User

# Create your models here.


STATE_CHOICES = (
   ('Lahore', 'Lahore'),
   ('Karachi', 'Karachi'),
   ('Islamabad', 'Islamabad'),
   ('Peshawar', 'Peshawar'),
   ('Quetta', 'Quetta'),
   ('Rawalpindi', 'Rawalpindi'),
   ('Faisalabad', 'Faisalabad'),
   ('Multan', 'Multan'),
   ('Gujranwala', 'Gujranwala'),
   ('Gujrat', 'Gujrat'),
   ('Sialkot', 'Sialkot'),
   ('Sukkur', 'Sukkur'),
   ('Hyderabad', 'Hyderabad'),
   ('Nawabshah', 'Nawabshah'),
   ('Mirpurkhas', 'Mirpurkhas')
)

CATEGORY_CHOICES = (
    ('CR', 'CURD'),
    ('IC', 'ICE-CREAMS'),
    ('GH', 'GHEE'),
    ('CZ', 'CHEESE'),
    ('LS', 'LASSI'),
    ('PN', 'PANEER'),
    ('MS', 'MILK SHAKE'),
    ('ML', 'MILK')
)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending')
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField(blank=True, null=True)
    discounted_price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200)
    product_image = models.ImageField(upload_to='product')
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=200)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    jazzcash_order_id = models.CharField(max_length=200, blank=True, null=True)
    jazzcash_payment_status = models.CharField(max_length=200, blank=True, null=True)
    jazzcash_payment_id = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")    

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

  

    
