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
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = TestimonialsMessage
        fields = ["id", "name", "title", "testimonial", "image"]


class LeadershipMessageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = LeadershipMessage
        fields = ["id", "salutation", "name", "designation", "message", "image"]


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = GalleryImage
        fields = ["id", "title", "image"]


class FeeStructureSerializer(serializers.ModelSerializer):
    tuition_per_term = serializers.DecimalField(max_digits=12, decimal_places=2)
    meals_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    transport_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    file = serializers.SerializerMethodField(allow_null=True)

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
        if obj.fee_structure_file:
            return obj.fee_structure_file.url
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
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = FeaturedEvent
        fields = ["id", "title", "date", "image", "description"]

    def get_date(self, obj):
        return obj.get_date_range_display() if hasattr(obj, "get_date_range_display") else None


class AlumniMessageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = AlumniMessage
        fields = ["id", "name", "title", "year_of_completion", "message", "image"]


class KeyAdmissionDeadlineSerializer(serializers.ModelSerializer):
    deadline_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)

    class Meta:
        model = KeyAdmissionDeadline
        fields = ["id", "name", "deadline_date"]


# ==============================
# WRITE SERIALIZERS (FORM SUBMISSIONS)
# ==============================

class AdmissionMessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=True)
    message = serializers.CharField(max_length=1000, required=True)

    class Meta:
        model = AdmissionMessage
        fields = ["name", "email", "phone", "message"]

    def validate(self, attrs):
        # Example: custom validation logic
        # if some_condition:
        #     raise serializers.ValidationError("Custom validation failed.")
        return attrs

    def create(self, validated_data):
        return AdmissionMessage.objects.create(**validated_data)


class EnquiryMessagesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=150, required=True)
    message = serializers.CharField(max_length=1000, required=True)

    class Meta:
        model = EnquiryMessages
        fields = ["name", "email", "subject", "message"]

    def validate(self, attrs):
        # Example: custom validation logic
        return attrs

    def create(self, validated_data):
        return EnquiryMessages.objects.create(**validated_data)
