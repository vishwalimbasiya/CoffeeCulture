from django.contrib import admin
from django.urls import path,include
from CoffeeCulture import views

urlpatterns = [
    path('',views.index),
    path('profile/',views.profile,name='profile'),
    path('menu/',views.menu,name='menu'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('notes/',views.notes,name='notes'),
    path('userlogout/',views.userlogout,name='userlogout'),
]
