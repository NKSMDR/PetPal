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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from petpalapp import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    
    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='pages/password_reset.html',
        email_template_name='pages/password_reset_email.html',
        subject_template_name='pages/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pages/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pages/password_reset_confirm.html',
        success_url='/password-reset-complete/'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pages/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Change Password (for logged-in users)
    path('change-password/', views.change_password, name='change_password'),
    path('breeds/', views.breed_list, name='breed_list'),
    path('breeds/<slug:slug>/', views.breed_detail, name='breed_detail'),
    path('browse-pets/', views.browse_pets, name='browse_pets'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('sell-pet/', views.sell_pet_info, name='sell_pet'),
    path('sell-pet-form/', views.sell_pet_form, name='sell_pet_form'),
    path('my-pets/', views.my_pets, name='my_pets'),
    path('my-pets/delete/<int:pk>/', views.delete_pet, name='delete_pet'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/pet/<int:pk>/', views.marketplace_pet_detail, name='marketplace_pet_detail'),
    path('accessories/', views.accessories, name='accessories'),
     path('accessories/<slug:slug>/', views.accessory_detail, name='accessory_detail'),
    path('about-us/', views.about_us, name='about_us'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:pet_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:breed_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/clear/<str:source>/', views.clear_wishlist_section, name='clear_wishlist_section'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:product_type>/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<str:product_type>/<int:product_id>/', views.update_cart, name='update_cart'),
    # Payment URLs
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/<int:transaction_id>/', views.payment_success, name='payment_success'),
    path('payment/failure/<int:transaction_id>/', views.payment_failure, name='payment_failure'),
    # Order URLs
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    # Listing Payment URLs
    path('listing-payment/checkout/', views.listing_payment_checkout, name='listing_payment_checkout'),
    path('listing-payment/success/<int:payment_id>/', views.listing_payment_success, name='listing_payment_success'),
    path('listing-payment/failure/<int:payment_id>/', views.listing_payment_failure, name='listing_payment_failure'),
    # Cart sync URL
    path('sync-cart/', views.sync_cart, name='sync_cart'),
    # # Debug URL
    # path('debug-cart/', views/debug_cart, name='debug_cart'),
    path('get-product-stock/<str:product_type>/<int:product_id>/', views.get_product_stock, name='get_product_stock'),

    # Chat API endpoints
    path('chat/messages/', views.chat_messages, name='chat_messages'),
    path('chat/send/', views.chat_send_message, name='chat_send_message'),

    # Generic thread-based chat APIs (for inbox)
    path('chat/threads/', views.chat_threads, name='chat_threads'),
    path('chat/thread/messages/', views.chat_thread_messages, name='chat_thread_messages'),
    path('chat/thread/send/', views.chat_thread_send, name='chat_thread_send'),
    
    # Earning Report
    path('admin-earning-report/', views.earning_report_detail, name='earning_report_detail'),
]