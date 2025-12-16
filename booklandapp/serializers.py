from rest_framework import serializers
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


# ------------------------------
# Content serializers (READ)
# ------------------------------
class TestimonialsMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialsMessage
        fields = ["id", "name", "title", "testimonial", "image"]


class LeadershipMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipMessage
        fields = ["id", "salutation", "name", "designation", "message", "image"]


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["id", "title", "image"]


class FeeStructureSerializer(serializers.ModelSerializer):
    tuition_per_term = serializers.FloatField()
    meals_fee = serializers.FloatField()
    transport_fee = serializers.FloatField()
    total_fee = serializers.FloatField()
    file = serializers.CharField(source="fee_structure_file")

    class Meta:
        model = FeeStructure
        fields = ["id", "level", "tuition_per_term", "meals_fee", "transport_fee", "total_fee", "file"]


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "title", "category", "month", "day", "year", "start_time", "end_time", "location",
                  "description"]

    def get_start_time(self, obj):
        return obj.start_time.strftime("%I:%M %p") if obj.start_time else None

    def get_end_time(self, obj):
        return obj.end_time.strftime("%I:%M %p") if obj.end_time else None


class FeaturedEventSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedEvent
        fields = ["id", "title", "date", "image", "description"]

    def get_date(self, obj):
        return obj.get_date_range_display()


class AlumniMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniMessage
        fields = ["id", "name", "title", "year_of_completion", "message", "image"]


class KeyAdmissionDeadlineSerializer(serializers.ModelSerializer):
    deadline_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = KeyAdmissionDeadline
        fields = ["id", "name", "deadline_date"]


# ------------------------------
# Form submission serializers (WRITE)
# ------------------------------
class AdmissionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionMessage
        fields = ["name", "email", "phone", "message"]


class EnquiryMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryMessages
        fields = ["name", "email", "subject", "message"]
