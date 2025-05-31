from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist

# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'category', 'product_image']

admin.site.register(Product, ProductModelAdmin)

class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'mobile', 'state', 'zipcode']
    list_filter = ['state', 'city']
    search_fields = ['user__username', 'locality', 'city', 'state']

admin.site.register(Customer, CustomerModelAdmin)



class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_cost']

admin.site.register(Cart, CartModelAdmin)


class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'jazzcash_order_id', 'jazzcash_payment_status', 'jazzcash_payment_id', 'paid']

admin.site.register(Payment, PaymentModelAdmin)


class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']

admin.site.register(OrderPlaced, OrderPlacedModelAdmin)


class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']

admin.site.register(Wishlist, WishlistModelAdmin)










