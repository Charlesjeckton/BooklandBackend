from rest_framework import serializers
from decimal import Decimal
from cloudinary.utils import cloudinary_url
import time

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
            "id", "level", "tuition_per_term", "meals_fee",
            "transport_fee", "total_fee", "file"
        ]

    def get_file(self, obj):
        if not obj.fee_structure_file:
            return None

        try:
            # Get ONLY the public_id, not the full URL
            # For CloudinaryField, use the .public_id attribute
            public_id = obj.fee_structure_file.public_id

            # If public_id is None or empty, try parsing from the field value
            if not public_id:
                # Extract public_id from the stored value
                field_value = str(obj.fee_structure_file)
                if '/upload/' in field_value:
                    # Extract everything after /upload/
                    parts = field_value.split('/upload/')
                    if len(parts) > 1:
                        public_id = parts[1].split('.')[0]  # Remove file extension

            if not public_id:
                return None

            # Generate proper signed URL
            url, _ = cloudinary_url(
                public_id,
                resource_type="raw",  # For PDF files
                type="authenticated",  # For private downloads
                sign_url=True,
                secure=True,
                expires_at=int(time.time()) + 3600  # 1 hour expiry
            )

            return url

        except Exception as e:
            print(f"Error generating Cloudinary URL: {e}")
            # Fallback: return direct URL if signed URL fails
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
