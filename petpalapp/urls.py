"""?
URL configuration for petpalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from petpalapp import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('breeds/', views.breed_list, name='breed_list'),
    path('breeds/<slug:slug>/', views.breed_detail, name='breed_detail'),
    path('browse-pets/', views.browse_pets, name='browse_pets'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('sell-pet/', views.sell_pet_info, name='sell_pet'),
    path('sell-pet-form/', views.sell_pet_form, name='sell_pet_form'),
    path('my-pets/', views.my_pets, name='my_pets'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/pet/<int:pk>/', views.marketplace_pet_detail, name='marketplace_pet_detail'),
    path('accessories/', views.accessories, name='accessories'),
     path('accessories/<slug:slug>/', views.accessory_detail, name='accessory_detail'),
    path('about-us/', views.about_us, name='about_us'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:product_type>/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<str:product_type>/<int:product_id>/', views.update_cart, name='update_cart'),
    # Payment URLs
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/<int:transaction_id>/', views.payment_success, name='payment_success'),
    path('payment/failure/<int:transaction_id>/', views.payment_failure, name='payment_failure'),
    # Listing Payment URLs
    path('listing-payment/checkout/', views.listing_payment_checkout, name='listing_payment_checkout'),
    path('listing-payment/success/<int:payment_id>/', views.listing_payment_success, name='listing_payment_success'),
    path('listing-payment/failure/<int:payment_id>/', views.listing_payment_failure, name='listing_payment_failure'),
    # Cart sync URL
    path('sync-cart/', views.sync_cart, name='sync_cart'),
    # # Debug URL
    # path('debug-cart/', views.debug_cart, name='debug_cart'),
    path('get-product-stock/<str:product_type>/<int:product_id>/', views.get_product_stock, name='get_product_stock'),
]