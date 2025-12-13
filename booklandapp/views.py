import calendar
from datetime import date

from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    AdmissionMessage,
    EnquiryMessages,
    TestimonialsMessage,
    LeadershipMessage,
    GalleryImage,
    FeeStructure,
    Event,
    AlumniMessage,
    FeaturedEvent,
    KeyAdmissionDeadline,
)


# ------------------------
# API VIEWS (JSON RESPONSE)
# ------------------------

def api_testimonials(request):
    """Return all testimonials as JSON"""
    testimonials = TestimonialsMessage.objects.all()
    data = [
        {
            "id": t.id,
            "name": t.name,
            "title": t.title,
            "testimonial": t.testimonial,
            "image": t.image.url if t.image else ""
        }
        for t in testimonials
    ]
    return JsonResponse(data, safe=False)


def api_events(request):
    """Return upcoming or filtered events as JSON"""
    selected_month = request.GET.get('month')
    selected_category = request.GET.get('category')

    events_qs = Event.objects.all()
    if selected_month:
        events_qs = events_qs.filter(month=selected_month)
    if selected_category:
        events_qs = events_qs.filter(category=selected_category)

    events = events_qs.order_by('-year', 'month', 'day')
    data = [
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "location": e.location,
            "day": e.day,
            "month": e.month,
            "year": e.year,
            "category": e.category
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)


def api_leadership(request):
    """Return leadership team as JSON"""
    team = LeadershipMessage.objects.all()
    data = [
        {
            "id": l.id,
            "name": l.name,
            "designation": l.designation,
            "image": l.image.url if l.image else ""
        }
        for l in team
    ]
    return JsonResponse(data, safe=False)


def api_gallery(request):
    """Return gallery images as JSON"""
    images = GalleryImage.objects.all()
    data = [{"id": g.id, "image": g.image.url if g.image else "", "caption": g.caption} for g in images]
    return JsonResponse(data, safe=False)


def api_fees(request):
    """Return fee structures as JSON"""
    fees = FeeStructure.objects.all()
    data = [{"id": f.id, "name": f.name, "amount": f.amount, "description": f.description} for f in fees]
    return JsonResponse(data, safe=False)


# ------------------------
# TEMPLATE VIEWS
# ------------------------

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def admissions(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')

        if not name or not email or not message_text:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('admissions')

        AdmissionMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )
        messages.success(request, 'Your request has been submitted successfully!')
        return redirect('admissions')

    deadlines = KeyAdmissionDeadline.objects.all()
    return render(request, 'admissions.html', {'deadlines': deadlines})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        EnquiryMessages.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')


def alumni(request):
    alumni_list = AlumniMessage.objects.all()
    return render(request, 'alumni.html', {'alumni_list': alumni_list})


def events(request):
    return render(request, 'events.html')


def faqs(request):
    return render(request, 'faqs.html')


def fees(request):
    return render(request, 'fees.html')
