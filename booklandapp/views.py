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
from .serializers import (
    TestimonialsMessageSerializer,
    LeadershipMessageSerializer,
    GalleryImageSerializer,
    FeeStructureSerializer,
    EventSerializer,
    FeaturedEventSerializer,
    AlumniMessageSerializer,
    KeyAdmissionDeadlineSerializer,
    AdmissionMessageSerializer,
    EnquiryMessagesSerializer,
)
from datetime import date

# =====================================================
# General / Health Check
# =====================================================
@api_view(["GET"])
def api_home(request):
    return Response({
        "name": "Bookland Schools API",
        "status": "running",
        "date": date.today()
    })


# =====================================================
# Read-only APIs
# =====================================================
@api_view(["GET"])
def api_testimonials(request):
    queryset = TestimonialsMessage.objects.all()
    serializer = TestimonialsMessageSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_leadership(request):
    queryset = LeadershipMessage.objects.all()
    serializer = LeadershipMessageSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_gallery(request):
    queryset = GalleryImage.objects.all()
    serializer = GalleryImageSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_fees(request):
    queryset = FeeStructure.objects.all()
    serializer = FeeStructureSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_events(request):
    queryset = Event.objects.all()
    month = request.GET.get("month")
    category = request.GET.get("category")
    if month:
        queryset = queryset.filter(month=month)
    if category:
        queryset = queryset.filter(category=category)
    queryset = queryset.order_by("-year", "month", "day")
    serializer = EventSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_featured_events(request):
    queryset = FeaturedEvent.objects.all()
    serializer = FeaturedEventSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_alumni(request):
    queryset = AlumniMessage.objects.all()
    serializer = AlumniMessageSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_admission_deadlines(request):
    queryset = KeyAdmissionDeadline.objects.all().order_by('deadline_date')
    serializer = KeyAdmissionDeadlineSerializer(queryset, many=True)
    return Response(serializer.data)


# =====================================================
# Write APIs
# =====================================================
@api_view(["POST"])
def api_admissions(request):
    serializer = AdmissionMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": "Admission request submitted successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def api_contact(request):
    serializer = EnquiryMessagesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": "Your message has been sent successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
