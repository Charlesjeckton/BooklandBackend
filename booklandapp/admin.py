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
# Generic Admin Mixin for Image Preview
# =====================================================
class ImagePreviewAdminMixin:
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Testimonials Admin
# =====================================================
@admin.register(TestimonialsMessage)
class TestimonialsMessageAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = TestimonialsMessageForm
    list_display = ("name", "title", "testimonial", "image_preview")


# =====================================================
# Leadership Admin
# =====================================================
@admin.register(LeadershipMessage)
class LeadershipMessageAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = LeadershipMessageForm
    list_display = ("salutation", "name", "designation", "message", "image_preview")


# =====================================================
# Alumni Admin
# =====================================================
@admin.register(AlumniMessage)
class AlumniMessageAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = AlumniMessageForm
    list_display = ("name", "title", "year_of_completion", "message", "image_preview")


# =====================================================
# Gallery Image Admin
# =====================================================
@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = GalleryImageForm
    list_display = ("title", "image_preview")


# =====================================================
# Featured Event Admin
# =====================================================
@admin.register(FeaturedEvent)
class FeaturedEventAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = FeaturedEventForm
    list_display = ("title", "start_date", "end_date", "image_preview")


# =====================================================
# Fee Structure Admin (with PDF download & preview)
# =====================================================
@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    form = FeeStructureForm

    list_display = (
        "level",
        "tuition_per_term",
        "meals_fee",
        "transport_fee",
        "total_fee",
        "file_link",
        "preview_link",
    )
    readonly_fields = ("file_link", "preview_link")
    list_filter = ("level",)
    search_fields = ("level",)

    fieldsets = (
        ("Fee Information", {
            "fields": ("level", "tuition_per_term", "meals_fee", "transport_fee", "total_fee")
        }),
        ("PDF Document", {
            "fields": ("fee_structure_file", "file_link", "preview_link"),
            "description": "Upload PDF file (max 10MB). File will be publicly accessible."
        }),
    )

    def file_link(self, obj):
        if obj.fee_structure_file:
            url = obj.fee_structure_file.url
            return format_html(
                '<a href="{}" target="_blank" style="background: #28a745; '
                'color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; '
                'font-weight: bold;">⬇️ Download PDF</a>',
                url
            )
        return format_html('<span style="color: #dc3545;">No PDF uploaded</span>')

    file_link.short_description = "Download"

    def preview_link(self, obj):
        if obj.fee_structure_file:
            url = obj.fee_structure_file.url
            return format_html(
                '<a href="{}" target="_blank" style="background: #17a2b8; '
                'color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; '
                'margin-left: 10px;">👁️ Preview PDF</a>',
                url
            )
        return ""

    preview_link.short_description = "Preview"


# =====================================================
# Standard models (no images or PDFs, default admin)
# =====================================================
admin.site.register(AdmissionMessage)
admin.site.register(EnquiryMessages)
admin.site.register(Event)
admin.site.register(KeyAdmissionDeadline)
