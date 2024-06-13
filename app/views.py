from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import (CustomerRegistrationForm,CustomerProfileForm, MyPasswordChangeForm)
from django.views import View
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from .models import (Customer,
                     Product,
                     Cart,
                     OrderPlaced)
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .forms import ProductForm
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from .models import BlogPost

# def home(request):
#  return render(request, 'app/home.html')


def cart_count(request): # NO url associated with this 
 cartcount = Cart.objects.filter(user=request.user).count()
 return cartcount

from django.shortcuts import render
from django.views import View
from .models import Product  # Ensure you import the Product model

class ProductView(View):
    def get(self, request):
        # Existing categories
        clothes = Product.objects.filter(category='CL')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        desktops = Product.objects.filter(category='D')
        # New categories
        electronics = Product.objects.filter(category='E')
        fashions = Product.objects.filter(category='FA')
        home_kitchen_items = Product.objects.filter(category='HK')
        beauty_personal_care = Product.objects.filter(category='BC')
        health_items = Product.objects.filter(category='HW')
        media_items = Product.objects.filter(category='BM')
        toys_games_items = Product.objects.filter(category='TG')
        sports_outdoors_items = Product.objects.filter(category='SO')
        baby_kids_items = Product.objects.filter(category='BK')
        cars = Product.objects.filter(category='C')
        grocery_items = Product.objects.filter(category='G')
        office_items = Product.objects.filter(category='OS')
        jewelry_items = Product.objects.filter(category='JW')
        home_tools_items = Product.objects.filter(category='HI')

        # Get cart count if the user is authenticated
        if request.user.is_authenticated:
            cartcount = cart_count(request)
        else:
            cartcount = ''

        context = {
            'clothes': clothes,
            'mobiles': mobiles, 'laptops': laptops,
            'electronics': electronics, 'fashions': fashions,
            'home_kitchen_items': home_kitchen_items, 'beauty_personal_care': beauty_personal_care,
            'health_items': health_items, 'media_items': media_items,
            'toys_games_items': toys_games_items, 'sports_outdoors_items': sports_outdoors_items,
            'baby_kids_items': baby_kids_items, 'cars': cars,
            'grocery_items': grocery_items, 'office_items': office_items,
            'jewelry_items': jewelry_items, 'home_tools_items': home_tools_items,
            'cartcount': cartcount, 'desktops': desktops
        }
        
        return render(request, 'app/home.html', context)

  
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
 
class ProductDetailView(View):
 def get(self,request,pk):
  if request.user.is_authenticated:
   cartcount = cart_count(request)
  else:
   cartcount = ''
  product = Product.objects.get(pk=pk)
  prod_already_in_cart = Cart.objects.filter(Q(product = product) & Q(user=request.user.id)).exists()
  # prod_already_in_cart = Cart.objects.filter(user=request.user,product = product)
 
  
  return render(request,'app/productdetail.html',{'product':product,'prod_already_in_cart':prod_already_in_cart,'cartcount':cartcount})
 
@login_required()
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod-id',None)
  if product_id:
    product_instance = Product.objects.get(id = product_id)
    cart_item = Cart.objects.filter(user = user, product = product_instance)
    
    if cart_item.exists():
      return redirect(reverse('showcart'))
    else:
      Cart(user = user, product=product_instance).save()
      messages.info(request, 'Product Added into Cart.')
    return redirect(reverse('showcart'))
  else:
   return redirect(reverse('home'))

# def add_to_cart_optional(request):
#     user = request.user
#     product_id = request.GET.get('prod-id')
#     product_instance = get_object_or_404(Product, id=product_id)
#     cart_item, created = Cart.objects.update_or_create(
#         user=user,
#         product=product_instance,
#         defaults={'quantity': 1},
#     )
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect(reverse('showcart'))
@login_required()
def show_cart(request):
  user = request.user
  cart_obj = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  # cart_product = [p for p in Cart.objects.all() if p.user == user ]
  cart_product = [p for p in Cart.objects.all() if p.user == user ]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      totalamount = amount + shipping_amount
    return render(request, 'app/addtocart.html',{'carts':cart_obj, 'totalamount': totalamount,'amount': amount,'cartcount':cart_count(request)}) 
  else:
    return render(request,'app/emptycart.html',{'cartcount':cart_count(request)})
 
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
  c.quantity+=1
  c.save()
  amount = 0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
 

  data = {
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':amount + shipping_amount
  }
  return JsonResponse(data)
 
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))

  if c.quantity > 1:
    c.quantity -= 1
    c.save()

  amount = 0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':amount + shipping_amount
  }
  return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
  c.delete()

  amount = 0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':amount + shipping_amount,
   'cartcount':cart_count(request)
  }
  return JsonResponse(data) 
 
  
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@login_required()
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add, 'active':'btn-primary','cartcount':cart_count(request)})

@login_required()
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'orderplaced':op,'cartcount':cart_count(request)})

# @login_required()
# def change_password(request):
#  cartcount = cart_count(request)
#  print('-------------',cartcount)
#  return render(request, 'app/changepassword.html',{'cartcount':cartcount})

def  mobile(request,data = None):
 if request.user.is_authenticated:
  cartcount = cart_count(request)
 else:
  cartcount = ''
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data in ('Samsung','Redmi','IQOO','Iphone','OnePlus'):
  mobiles = Product.objects.filter(category='M').filter(brand = data) 
 elif data == 'below_10k':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above_10k':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

 return render(request, 'app/mobile.html',{'mobiles':mobiles,'cartcount':cartcount})

def laptop(request,data = None):
 if request.user.is_authenticated:
  cartcount = cart_count(request)
 else:
  cartcount = ''
   
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data in ('ASUS','HP','Dell','MSI'):
  laptops = Product.objects.filter(category='L').filter(brand = data) 
 elif data == 'below_40k':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
 elif data == 'above_40k':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=40000)

 return render(request, 'app/laptop.html',{'laptops':laptops,'cartcount':cartcount})

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request,'Congratulations! Registration Successfully')
   return redirect(reverse('login'))
  return render(request,'app/customerregistration.html',{'form':form})

@login_required()
def checkout(request):
 user = request.user
 address = Customer.objects.filter(user = user)
 cart_items = Cart.objects.filter(user = user)
 amount = 0
 shipping_amount = 70.0
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user ]

 if cart_product:
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
  total_amount = amount + shipping_amount
 return render(request, 'app/checkout.html',{'address':address,'total_amount':total_amount,'cart_items':cart_items,'cartcount':cart_count(request)    })

@login_required()
def payment_done(request):
 if request.method == "GET":
  user = request.user
  custid= request.GET.get('custid',None)
  if custid:
    customer = Customer.objects.get(id=custid)
    cart_items = Cart.objects.filter(user=user)
    for c in cart_items:
      order_placed = OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity)
      order_placed.save()
      c.delete()
  return redirect(reverse('orders'))


class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next' 

    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary','cartcount':cart_count(request)})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!!! Address Saved Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary','cartcount':cart_count(request)})



class MyPasswordChangeView(PasswordChangeView):
    template_name = 'app/passwordchange.html'
    form_class = MyPasswordChangeForm
    success_url = '/passwordchangedone/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cartcount'] = cart_count(self.request)
        return context
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'app/passwordchangedone.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cartcount'] = cart_count(self.request)
        return context
      
def desktop(request,data = None):
 if request.user.is_authenticated:
  cartcount = cart_count(request)
 else:
  cartcount = ''
   
 if data == None:
  desktops = Product.objects.filter(category='D')
 elif data in ('ASUS','HP','Dell','MSI'):
  desktops = Product.objects.filter(category='D').filter(brand = data) 
 elif data == 'below_40k':
  desktops = Product.objects.filter(category='D').filter(discounted_price__lt=40000)
 elif data == 'above_40k':
  desktops = Product.objects.filter(category='D').filter(discounted_price__gt=40000)

 return render(request, 'app/desktop.html',{'desktops':desktops,'cartcount':cartcount})
    

def car(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # Assumed function to get the cart count
    else:
        cartcount = ''

    if data is None:
        cars = Product.objects.filter(category='C')  # Assuming 'C' stands for Cars
    elif data in ('Toyota', 'Honda', 'Ford', 'Chevrolet'):
        cars = Product.objects.filter(category='C').filter(brand=data)
    elif data == 'below_500k':
        cars = Product.objects.filter(category='C').filter(discounted_price__lt=500000)
    elif data == 'above_500k':
        cars = Product.objects.filter(category='C').filter(discounted_price__gt=500000)

    return render(request, 'app/car.html', {'cars': cars, 'cartcount': cartcount})
  

def electronic(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function needs to exist to get the cart count
    else:
        cartcount = ''

    if data is None:
        electronics = Product.objects.filter(category='E')  # Assuming 'E' stands for Electronics
    elif data in ('Samsung', 'Apple', 'Sony', 'LG'):
        electronics = Product.objects.filter(category='E').filter(brand=data)
    elif data == 'below_20k':
        electronics = Product.objects.filter(category='E').filter(discounted_price__lt=20000)
    elif data == 'above_20k':
        electronics = Product.objects.filter(category='E').filter(discounted_price__gt=20000)

    return render(request, 'app/electronic.html', {'electronics': electronics, 'cartcount': cartcount})


def fashion(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function needs to exist to get the cart count
    else:
        cartcount = ''

    if data is None:
        fashions = Product.objects.filter(category='FA')  # Assuming 'FA' stands for Fashion and Apparel
    elif data in ('Zara', 'HM', 'Nike', 'Adidas'):
        fashions = Product.objects.filter(category='FA').filter(brand=data)
    elif data == 'below_1000':
        fashions = Product.objects.filter(category='FA').filter(discounted_price__lt=1000)
    elif data == 'above_1000':
        fashions = Product.objects.filter(category='FA').filter(discounted_price__gt=1000)

    return render(request, 'app/fashion.html', {'fashions': fashions, 'cartcount': cartcount})


def home_kitchen(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # Ensure this function exists to get the cart count
    else:
        cartcount = ''

    if data is None:
        home_kitchen_items = Product.objects.filter(category='HK')  # 'HK' stands for Home and Kitchen Appliance
    elif data in ('Philips', 'Samsung', 'Bosch', 'Whirlpool'):
        home_kitchen_items = Product.objects.filter(category='HK').filter(brand=data)
    elif data == 'below_5000':
        home_kitchen_items = Product.objects.filter(category='HK').filter(discounted_price__lt=5000)
    elif data == 'above_5000':
        home_kitchen_items = Product.objects.filter(category='HK').filter(discounted_price__gt=5000)

    return render(request, 'app/home_kitchen.html', {'home_kitchen_items': home_kitchen_items, 'cartcount': cartcount})


def beauty_personal_care(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function needs to exist to get the cart count
    else:
        cartcount = ''

    if data is None:
        beauty_items = Product.objects.filter(category='BC')  # 'BC' stands for Beauty and Personal Care
    elif data in ('Oreal', 'Nivea', 'Estee_Lauder', 'Clinique'):
        beauty_items = Product.objects.filter(category='BC').filter(brand=data)
    elif data == 'below_1000':
        beauty_items = Product.objects.filter(category='BC').filter(discounted_price__lt=1000)
    elif data == 'above_1000':
        beauty_items = Product.objects.filter(category='BC').filter(discounted_price__gt=1000)

    return render(request, 'app/beauty.html', {'beauty_items': beauty_items, 'cartcount': cartcount})


def health_wellness(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function needs to be implemented to track the cart count
    else:
        cartcount = ''

    if data is None:
        health_items = Product.objects.filter(category='HW')  # 'HW' stands for Health and Wellness
    elif data in ('GNC', 'Optimum_Nutrition', 'Herbalife', 'Nature_Made'):
        health_items = Product.objects.filter(category='HW').filter(brand=data)
    elif data == 'below_500':
        health_items = Product.objects.filter(category='HW').filter(discounted_price__lt=500)
    elif data == 'above_500':
        health_items = Product.objects.filter(category='HW').filter(discounted_price__gt=500)

    return render(request, 'app/health_wellness.html', {'health_items': health_items, 'cartcount': cartcount})


def books_movies_music(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # Ensure this function exists to get the cart count
    else:
        cartcount = ''

    # Filter by type
    if data is None:
        media_items = Product.objects.filter(category='BMM')  # 'BMM' stands for Books, Movies, and Music
    elif data == 'books':
        media_items = Product.objects.filter(category='BMM', brand='book')
    elif data == 'movies':
        media_items = Product.objects.filter(category='BMM', brand='movie')
    elif data == 'music':
        media_items = Product.objects.filter(category='BMM', brand='music')
    elif data == 'below_100':
        media_items = Product.objects.filter(category='BMM', discounted_price__lt=100)
    elif data == 'above_100':
        media_items = Product.objects.filter(category='BMM', discounted_price__gt=100)

    return render(request, 'app/books_movies_music.html', {'media_items': media_items, 'cartcount': cartcount})


def toys_games(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function needs to be implemented to track the cart count
    else:
        cartcount = ''

    if data is None:
        toys_games_items = Product.objects.filter(category='TG')  # 'TG' stands for Toys and Games
    elif data in ('board_games', 'electronic_games', 'action_figures'):
        toys_games_items = Product.objects.filter(category='TG', brand = data)
    elif data == 'below_500':
        toys_games_items = Product.objects.filter(category='TG', discounted_price__lt=500)
    elif data == 'above_500':
        toys_games_items = Product.objects.filter(category='TG', discounted_price__gt=500)

    return render(request, 'app/toys_games.html', {'toys_games_items': toys_games_items, 'cartcount': cartcount})



def sports_outdoors(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # Ensure this function exists to get the cart count
    else:
        cartcount = ''

    if data is None:
        sports_outdoors_items = Product.objects.filter(category='SO')  # 'SO' stands for Sports and Outdoors
    elif data in ('soccer', 'basketball', 'camping'):
        sports_outdoors_items = Product.objects.filter(category='SO', brand = data)
    elif data == 'below_1000':
        sports_outdoors_items = Product.objects.filter(category='SO', discounted_price__lt=1000)
    elif data == 'above_1000':
        sports_outdoors_items = Product.objects.filter(category='SO', discounted_price__gt=1000)

    return render(request, 'app/sports_outdoors.html', {'sports_outdoors_items': sports_outdoors_items, 'cartcount': cartcount})



def baby_kids(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # Ensure this function exists to get the cart count
    else:
        cartcount = ''

    if data is None:
        baby_kids_items = Product.objects.filter(category='BK')  # 'BK' stands for Baby and Kids
    elif data in ('toys', 'clothes', 'accessories'):
        baby_kids_items = Product.objects.filter(category='BK', brand = data)
    elif data == 'below_500':
        baby_kids_items = Product.objects.filter(category='BK', discounted_price__lt=500)
    elif data == 'above_500':
        baby_kids_items = Product.objects.filter(category='BK', discounted_price__gt=500)

    return render(request, 'app/baby_kids.html', {'baby_kids_items': baby_kids_items, 'cartcount': cartcount})


def groceries_household(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # Ensure this function exists to get the cart count
    else:
        cartcount = ''

    if data is None:
        grocery_items = Product.objects.filter(category='GH')  # 'GH' stands for Groceries and Household Essentials
    elif data in ('food', 'cleaning', 'toiletries'):
        grocery_items = Product.objects.filter(category='GH', brand = data)
    elif data == 'below_200':
        grocery_items = Product.objects.filter(category='GH', discounted_price__lt=200)
    elif data == 'above_200':
        grocery_items = Product.objects.filter(category='GH', discounted_price__gt=200)

    return render(request, 'app/groceries_household.html', {'grocery_items': grocery_items, 'cartcount': cartcount})


def office_supplies(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function should be implemented to get the cart count
    else:
        cartcount = ''

    if data is None:
        office_items = Product.objects.filter(category='OS')  # 'OS' stands for Office Supplies
    elif data in ('stationery', 'furniture', 'technology'):
        office_items = Product.objects.filter(category='OS', brand = data)
    elif data == 'below_1000':
        office_items = Product.objects.filter(category='OS', discounted_price__lt=1000)
    elif data == 'above_1000':
        office_items = Product.objects.filter(category='OS', discounted_price__gt=1000)

    return render(request, 'app/office_supplies.html', {'office_items': office_items, 'cartcount': cartcount})


def jewelry_watches(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function should be implemented to get the cart count
    else:
        cartcount = ''

    if data is None:
        jewelry_items = Product.objects.filter(category='JW')  # 'JW' stands for Jewelry and Watches
    elif data in ('necklaces', 'earrings', 'watches'):
        jewelry_items = Product.objects.filter(category='JW', brand = data)
    elif data == 'gold':
        jewelry_items = Product.objects.filter(category='JW', material='gold')
    elif data == 'silver':
        jewelry_items = Product.objects.filter(category='JW', material='silver')
    elif data == 'below_5000':
        jewelry_items = Product.objects.filter(category='JW', discounted_price__lt=5000)
    elif data == 'above_5000':
        jewelry_items = Product.objects.filter(category='JW', discounted_price__gt=5000)

    return render(request, 'app/jewelry_watches.html', {'jewelry_items': jewelry_items, 'cartcount': cartcount})


def home_improvement_tools(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function should be implemented to track the cart count
    else:
        cartcount = ''

    if data is None:
        home_tools_items = Product.objects.filter(category='HI')  # 'HI' stands for Home Improvement and Tools
    elif data in ('tools', 'building_materials', 'hardware'):
        home_tools_items = Product.objects.filter(category='HI', brand = data)
    elif data == 'below_1000':
        home_tools_items = Product.objects.filter(category='HI', discounted_price__lt=1000)
    elif data == 'above_1000':
        home_tools_items = Product.objects.filter(category='HI', discounted_price__gt=1000)

    return render(request, 'app/home_improvement_tools.html', {'home_tools_items': home_tools_items, 'cartcount': cartcount})


def clothe(request, data=None):
    if request.user.is_authenticated:
        cartcount = cart_count(request)  # This function should be implemented to track the cart count
    else:
        cartcount = ''

    if data is None:
        clothes = Product.objects.filter(category='CL')  # 'CL' stands for Clothes
    elif data in ('mens_wear', 'womens_wear', 'childrens_wear','Nike'):
        clothes = Product.objects.filter(category='CL', brand = data)
    elif data == 'below_1000':
        clothes = Product.objects.filter(category='CL', discounted_price__lt=1000)
    elif data == 'above_1000':
        clothes = Product.objects.filter(category='CL', discounted_price__gt=1000)

    return render(request, 'app/clothe.html', {'clothes': clothes, 'cartcount': cartcount})

@login_required()
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('list_products')  # Redirect to the product listing view
    else:
        form = ProductForm()
    return render(request, 'app/product_form.html', {'form': form})

@login_required()
def list_products(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'app/product_list.html', {'products': products})

@login_required()
def update_product(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'app/product_form.html', {'form': form})


@login_required()
def delete_product(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')
    return render(request, 'app/product_confirm_delete.html', {'product': product})

# contact/views.py
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.urls import reverse_lazy

class SuccessView(TemplateView):
    template_name = 'app/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_data'] = self.request.session.get('contact_data', {})
        return context

class ContactView(FormView):
    template_name = 'app/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        # Here you can process the form data
        self.request.session['contact_data'] = form.cleaned_data
        return super().form_valid(form)

    def form_valid(self, form):
        # Implement any form processing here
        return super().form_valid(form)


from django.shortcuts import render
from .models import Product

def homepage(request):
    home_kitchen_items = Product.objects.filter(category='Home and Kitchen Appliance')
    return render(request, 'app/home.html', {'home_kitchen_items': home_kitchen_items})

def about_us(request):
    return render(request, 'app/about_us.html')

def payment_methods(request):
    return render(request, 'app/payment_method.html')

def money_back_guarantee(request):
    return render(request, 'app/money_back_guarantee.html')

def returns(request):
    return render(request, 'app/returns.html')

def shipping(request):
    return render(request, 'app/shipping.html')

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'app/blog_list.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'app/blog_detail.html', {'post': post})

def our_services(request):
    return render(request, 'app/our_services.html')