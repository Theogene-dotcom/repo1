from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import (LoginForm,MyPasswordChangeForm,MyPasswordResetForm, MySetPasswordForm)
from .views import ContactView, SuccessView
from .views import blog_list, blog_detail

urlpatterns = [
    # path('', views.home), 
    path('', views.ProductView.as_view(),name='home'),

    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart,   name='add-to-cart'),
    
    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdata/',views.payment_done,name='paymentdone'),
    
    path('buy/', views.buy_now, name='buy-now'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('address/', views.address, name='address'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/', views.list_products, name='list_products'),
    path('products/update/<int:id>/', views.update_product, name='update_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    
    path('car/', views.car, name='car'),
    path('car/<slug:data>', views.car, name='cardata'),
    
    path('desktop/', views.desktop, name='desktop'),
    path('desktop/<slug:data>', views.desktop, name='desktopdata'),
    
    path('electronic/', views.electronic, name='electronic'),
    path('electronic/<slug:data>', views.electronic, name='electronicdata'),
    
    path('fashion/', views.fashion, name='fashion'),
    path('fashion/<slug:data>', views.fashion, name='fashiondata'),
    
    path('home_kitchen/', views.home_kitchen, name='home_kitchen'),
    path('home_kitchen/<slug:data>', views.home_kitchen, name='home_kitchendata'),
    
    path('sports_outdoors/', views.sports_outdoors, name='sports_outdoors'),
    path('sports_outdoors/<slug:data>', views.sports_outdoors, name='sports_outdoorsdata'),
    
    path('beauty_personal_care/', views.beauty_personal_care, name='beauty_personal_care'),
    path('beauty_personal_care/<slug:data>', views.beauty_personal_care, name='beauty_personal_caredata'),
    
    path('health_wellness/', views.health_wellness, name='health_wellness'),
    path('health_wellness/<slug:data>', views.health_wellness, name='health_wellnessdata'),
    
    path('books_movies_music/', views.books_movies_music, name='books_movies_music'),
    path('books_movies_music/<slug:data>', views.books_movies_music, name='books_movies_musicdata'),
    
    path('toys_games/', views.toys_games, name='toys_games'),
    path('toys_games/<slug:data>', views.toys_games, name='toys_gamesdata'),
    
    path('baby_kids/', views.baby_kids, name='baby_kids'),
    path('baby_kids/<slug:data>', views.baby_kids, name='baby_kidsdata'),
    
    path('groceries_household/', views.groceries_household, name='groceries_household'),
    path('groceries_household/<slug:data>', views.groceries_household, name='groceries_householddata'),
    
    path('jewelry_watches/', views.jewelry_watches, name='jewelry_watches'),
    path('jewelry_watches/<slug:data>', views.jewelry_watches, name='jewelry_watchesdata'),
    
    path('clothe/', views.clothe, name='clothe'),
    path('clothe/<slug:data>', views.clothe, name='clothedata'),
    
    path('office_supplies/', views.office_supplies, name='office_supplies'),
    path('office_supplies/<slug:data>', views.office_supplies, name='office_suppliesdata'),
    
    path('home_improvement_tools/', views.home_improvement_tools, name='home_improvement_tools'),
    path('home_improvement_tools/<slug:data>', views.home_improvement_tools, name='home_improvement_toolsdata'),

    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),

    # path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchange/',views.MyPasswordChangeView.as_view(),name='passwordchange'),

    path('passwordchangedone/',views.MyPasswordChangeDoneView.as_view()),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    
    path('contact/', ContactView.as_view(), name='contact'),
    path('success/', SuccessView.as_view(), name='success'),
    path('about/', views.about_us, name='about_us'),
    path('payment-methods/', views.payment_methods, name='payment_methods'),
    path('money-back-guarantee/', views.money_back_guarantee, name='money_back_guarantee'),
    path('returns/', views.returns, name='returns'),
    path('shipping/', views.shipping, name='shipping'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('our-services/', views.our_services, name='our_services'),


] + static(settings.MEDIA_URL,document_root = settings
.MEDIA_ROOT)
