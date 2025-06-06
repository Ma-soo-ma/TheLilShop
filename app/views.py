from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced, Payment, Wishlist
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout



# Create your views here.
@login_required
def home(request):
    return render(request, "app/home.html")
@login_required
def about(request):
    return render(request, "app/about.html")
@login_required
def contact(request):
    return render(request, "app/contact.html")

@method_decorator(login_required, name='dispatch')
class categoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())


@method_decorator(login_required, name='dispatch')
class categoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())
        
@method_decorator(login_required, name='dispatch')
class productDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", locals())

@method_decorator(login_required, name='dispatch')
class customerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")

        messages.warning(request, "Invalid Input Data")
        return render(request, "app/customerregistration.html", locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        addresses = Customer.objects.filter(user=request.user)
        return render(request, "app/profile.html", locals())
        
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            # Create a new address entry instead of updating
            Customer.objects.create(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode
            )
            messages.success(request, "Congratulations! New Address Added Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        addresses = Customer.objects.filter(user=request.user)
        return render(request, "app/profile.html", locals())

def address(request):
        add = Customer.objects.filter(user=request.user)
        return render(request, "app/address.html",locals())
@method_decorator(login_required, name='dispatch')
class updateAddress(View):
        def get(self, request, pk):
            add = Customer.objects.get(pk=pk)
            form = CustomerProfileForm(instance=add)
            return render(request, "app/updateAddress.html",locals())
        def post(self, request, pk):
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                add = Customer.objects.get(pk=pk)   
                add.name = form.cleaned_data['name']                
                add.locality = form.cleaned_data['locality']
                add.city = form.cleaned_data['city']
                add.mobile = form.cleaned_data['mobile']
                add.state = form.cleaned_data['state']
                add.zipcode = form.cleaned_data['zipcode']

                add.save()
                messages.success(request, "Congratulations! Address Updated Successfully")
            else:
                messages.warning(request, "Invalid Input Data")

            return redirect("address")

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


     
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, "app/addtocart.html", locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        if not cart_items:
            return redirect('showcart')
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, "app/checkout.html", locals())

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        customer_id = request.POST.get('custid')
        if not customer_id:
            messages.warning(request, "Please select a shipping address")
            return redirect('checkout')
        
        cart_items = Cart.objects.filter(user=user)
        if not cart_items:
            return redirect('showcart')
            
        try:
            customer = Customer.objects.get(id=customer_id)
            # Here you would typically create an Order object and OrderItems
            # For now, we'll just clear the cart
            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('home')
        except Customer.DoesNotExist:
            messages.warning(request, "Selected address not found")
            return redirect('checkout')




def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "app/orders.html", locals())   


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
        
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()    
        user = request.user 
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
            

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=request.user, product=product).save()
        data = {
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(Q(product=product) & Q(user=user)).delete()
        data = {    
            'message':'Wishlist Removed Successfully',
        }
        return JsonResponse(data)

def show_wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html", locals())
@login_required
def search(request):
    query = request.GET.get('search')
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
   
    return render(request, "app/search.html", locals())





def logout_view(request):
    logout(request)
    return redirect('login')

