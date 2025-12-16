from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AdmissionMessage,
    EnquiryMessages,
    AlumniMessage,
    LeadershipMessage,
    TestimonialsMessage,
    FeeStructure,
    Event,
    FeaturedEvent,
    GalleryImage,
    KeyAdmissionDeadline,
)
from .forms import (
    TestimonialsMessageForm,
    LeadershipMessageForm,
    AlumniMessageForm,
    FeaturedEventForm,
    GalleryImageForm,
    FeeStructureForm,
)


# =====================================================
# Utility to display Cloudinary image previews
# =====================================================
def cloudinary_image_preview(obj, field_name):
    url = getattr(obj, field_name)
    if url:
        return format_html(
            '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />',
            url
        )
    return "No Image"


cloudinary_image_preview.short_description = "Preview"


# =====================================================
# Testimonials Admin
# =====================================================
@admin.register(TestimonialsMessage)
class TestimonialsMessageAdmin(admin.ModelAdmin):
    form = TestimonialsMessageForm
    list_display = ("name", "title", "testimonial", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Leadership Admin
# =====================================================
@admin.register(LeadershipMessage)
class LeadershipMessageAdmin(admin.ModelAdmin):
    form = LeadershipMessageForm
    list_display = ("salutation", "name", "designation", "message", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Alumni Admin
# =====================================================
@admin.register(AlumniMessage)
class AlumniMessageAdmin(admin.ModelAdmin):
    form = AlumniMessageForm
    list_display = ("name", "title", "year_of_completion", "message", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Gallery Image Admin
# =====================================================
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageForm
    list_display = ("title", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Featured Event Admin
# =====================================================
@admin.register(FeaturedEvent)
class FeaturedEventAdmin(admin.ModelAdmin):
    form = FeaturedEventForm
    list_display = ("title", "start_date", "end_date", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Fee Structure Admin (with PDF upload)
# =====================================================
@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    form = FeeStructureForm
    list_display = ("level", "tuition_per_term", "meals_fee", "transport_fee", "total_fee", "file_link")
    readonly_fields = ("file_link",)

    def file_link(self, obj):
        if obj.fee_structure_file:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.fee_structure_file)
        return "No PDF"

    file_link.short_description = "Fee Structure PDF"


# =====================================================
# Standard models (no images or PDFs, default admin)
# =====================================================
admin.site.register(AdmissionMessage)
admin.site.register(EnquiryMessages)
admin.site.register(Event)
admin.site.register(KeyAdmissionDeadline)
