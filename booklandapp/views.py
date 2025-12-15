from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
# GENERAL / HEALTH CHECK
# =====================================================

@api_view(["GET"])
def api_home(request):
    return Response({
        "name": "Bookland Schools API",
        "status": "running",
        "date": date.today()
    })


# =====================================================
# CONTENT APIs (READ)
# =====================================================

@api_view(["GET"])
def api_testimonials(request):
    data = [
        {
            "id": t.id,
            "name": t.name,
            "title": t.title,
            "testimonial": t.testimonial,
            "image": t.image.url if t.image else None,
        }
        for t in TestimonialsMessage.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
def api_leadership(request):
    data = [
        {
            "id": l.id,
            "salutation": l.salutation,
            "name": l.name,
            "designation": l.designation,
            "message": l.message,
            "image": l.image.url if l.image else None,
        }
        for l in LeadershipMessage.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
def api_gallery(request):
    data = [
        {
            "id": g.id,
            "title": g.title,
            "image": g.image.url if g.image else None,
        }
        for g in GalleryImage.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
def api_fees(request):
    data = [
        {
            "id": f.id,
            "level": f.level,
            "tuition_per_term": float(f.tuition_per_term),
            "meals_fee": float(f.meals_fee),
            "transport_fee": float(f.transport_fee),
            "total_fee": float(f.total_fee),
            "file": f.fee_structure_file.url if f.fee_structure_file else None,
        }
        for f in FeeStructure.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
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
    return Response(data)


@api_view(["GET"])
def api_featured_events(request):
    data = [
        {
            "id": f.id,
            "title": f.title,
            "date": f.get_date_range_display(),
            "image": f.image.url if f.image else None,
            "description": f.description,
        }
        for f in FeaturedEvent.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
def api_alumni(request):
    data = [
        {
            "id": a.id,
            "name": a.name,
            "title": a.title,
            "year_of_completion": a.year_of_completion,
            "message": a.message,
            "image": a.image.url if a.image else None,
        }
        for a in AlumniMessage.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
def api_admission_deadlines(request):
    data = [
        {
            "id": d.id,
            "title": d.title,
            "deadline": d.deadline,
            "description": d.description,
        }
        for d in KeyAdmissionDeadline.objects.all()
    ]
    return Response(data)


# =====================================================
# FORM SUBMISSION APIs (WRITE)
# =====================================================

@api_view(["POST"])
def api_admissions(request):
    name = request.data.get("name")
    email = request.data.get("email")
    phone = request.data.get("phone")
    message = request.data.get("message")

    if not name or not email or not message:
        return Response(
            {"error": "Name, email and message are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    AdmissionMessage.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message,
    )

    return Response(
        {"success": "Admission request submitted successfully."},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def api_contact(request):
    EnquiryMessages.objects.create(
        name=request.data.get("name"),
        email=request.data.get("email"),
        subject=request.data.get("subject"),
        message=request.data.get("message"),
    )

    return Response(
        {"success": "Your message has been sent successfully."},
        status=status.HTTP_201_CREATED,
    )
