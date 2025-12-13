from django.contrib import admin
from django.urls import path
import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admissions/', views.admissions, name='admissions'),
    path('alumni/', views.alumni, name='alumni'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),
    path('faqs/', views.faqs, name='faqs'),
    path('fees/', views.fees, name='fees'),
    path('admin/', admin.site.urls),
]
