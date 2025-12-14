from datetime import date
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


# =====================================================
# API VIEWS (JSON RESPONSES)
# =====================================================

def api_testimonials(request):
    data = [
        {
            "id": t.id,
            "name": t.name,
            "title": t.title,
            "testimonial": t.testimonial,
            "image": t.image.url if t.image else "",
        }
        for t in TestimonialsMessage.objects.all()
    ]
    return JsonResponse(data, safe=False)


def api_leadership(request):
    data = [
        {
            "id": l.id,
            "salutation": l.salutation,
            "name": l.name,
            "designation": l.designation,
            "message": l.message,
            "image": l.image.url if l.image else "",
        }
        for l in LeadershipMessage.objects.all()
    ]
    return JsonResponse(data, safe=False)


def api_gallery(request):
    data = [
        {
            "id": g.id,
            "title": g.title,
            "image": g.image.url if g.image else "",
        }
        for g in GalleryImage.objects.all()
    ]
    return JsonResponse(data, safe=False)


def api_fees(request):
    data = [
        {
            "id": f.id,
            "level": f.level,
            "tuition_per_term": float(f.tuition_per_term),
            "meals_fee": float(f.meals_fee),
            "transport_fee": float(f.transport_fee),
            "total_fee": float(f.total_fee),
            "file": f.fee_structure_file.url if f.fee_structure_file else "",
        }
        for f in FeeStructure.objects.all()
    ]
    return JsonResponse(data, safe=False)


def api_events(request):
    month = request.GET.get("month")
    category = request.GET.get("category")
    events_qs = Event.objects.all()
    if month:
        events_qs = events_qs.filter(month=month)
    if category:
        events_qs = events_qs.filter(category=category)
    events_qs = events_qs.order_by("-year", "month", "day")

    data = [
        {
            "id": e.id,
            "title": e.title,
            "category": e.category,
            "month": e.month,
            "day": e.day,
            "year": e.year,
            "start_time": e.start_time.strftime("%I:%M %p"),
            "end_time": e.end_time.strftime("%I:%M %p"),
            "location": e.location,
            "description": e.description,
        }
        for e in events_qs
    ]
    return JsonResponse(data, safe=False)


def api_featured_events(request):
    data = [
        {
            "id": f.id,
            "title": f.title,
            "date": f.get_date_range_display(),
            "image": f.image.url if f.image else "",
            "description": f.description,
        }
        for f in FeaturedEvent.objects.all()
    ]
    return JsonResponse(data, safe=False)


def api_alumni(request):
    data = [
        {
            "id": a.id,
            "name": a.name,
            "title": a.title,
            "year_of_completion": a.year_of_completion,
            "message": a.message,
            "image": a.image.url if a.image else "",
        }
        for a in AlumniMessage.objects.all()
    ]
    return JsonResponse(data, safe=False)


# =====================================================
# TEMPLATE (PAGE) VIEWS
# =====================================================

def index(request):
    # Page will fetch all dynamic data via API
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def admissions(request):
    deadlines = KeyAdmissionDeadline.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")

        if not name or not email or not message_text:
            messages.error(request, "Please fill in all required fields.")
            return redirect("admissions")

        AdmissionMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text,
        )
        messages.success(
            request, "Your admission request has been submitted successfully!"
        )
        return redirect("admissions")

    return render(request, "admissions.html", {"deadlines": deadlines})


def contact(request):
    if request.method == "POST":
        EnquiryMessages.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")


def alumni(request):
    # Page will fetch alumni via API
    return render(request, "alumni.html")


def events(request):
    # Page will fetch events and featured events via API
    return render(request, "events.html")


def fees(request):
    # Page will fetch fees via API
    return render(request, "fees.html")


def faqs(request):
    return render(request, "faqs.html")
