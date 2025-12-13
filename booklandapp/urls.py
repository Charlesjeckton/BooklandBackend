from django.urls import path
from . import views

urlpatterns = [
    # Template pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admissions/', views.admissions, name='admissions'),
    path('alumni/', views.alumni, name='alumni'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),
    path('faqs/', views.faqs, name='faqs'),
    path('fees/', views.fees, name='fees'),

    # API endpoints
    path('api/testimonials/', views.api_testimonials, name='api_testimonials'),
    path('api/events/', views.api_events, name='api_events'),
    path('api/leadership/', views.api_leadership, name='api_leadership'),
    path('api/gallery/', views.api_gallery, name='api_gallery'),
    path('api/fees/', views.api_fees, name='api_fees'),
]
