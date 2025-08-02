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
    path('accessories/', views.accessories, name='accessories'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:product_type>/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<str:product_type>/<int:product_id>/', views.update_cart, name='update_cart'),
]