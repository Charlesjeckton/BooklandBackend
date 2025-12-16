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


# ==============================
# READ SERIALIZERS
# ==============================
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
    tuition_per_term = serializers.DecimalField(max_digits=12, decimal_places=2)
    meals_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    transport_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    file = serializers.SerializerMethodField()

    class Meta:
        model = FeeStructure
        fields = [
            "id",
            "level",
            "tuition_per_term",
            "meals_fee",
            "transport_fee",
            "total_fee",
            "file",
        ]

    def get_file(self, obj):
        if not obj.fee_structure_file:
            return None

        # SIMPLE: Return public URL directly
        try:
            return obj.fee_structure_file.url
        except:
            return None


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "category",
            "month",
            "day",
            "year",
            "start_time",
            "end_time",
            "location",
            "description",
        ]

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


# ==============================
# WRITE SERIALIZERS
# ==============================

class AdmissionMessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=1000)

    class Meta:
        model = AdmissionMessage
        fields = ["name", "email", "phone", "message"]


class EnquiryMessagesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=150)
    message = serializers.CharField(max_length=1000)

    class Meta:
        model = EnquiryMessages
        fields = ["name", "email", "subject", "message"]
