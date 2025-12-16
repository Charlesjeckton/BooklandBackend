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
    list_display = ("title", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Featured Event Admin
# =====================================================
@admin.register(FeaturedEvent)
class FeaturedEventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return cloudinary_image_preview(obj, "image")


# =====================================================
# Other models (no images, standard registration)
# =====================================================
admin.site.register(AdmissionMessage)
admin.site.register(EnquiryMessages)
admin.site.register(FeeStructure)
admin.site.register(Event)
admin.site.register(KeyAdmissionDeadline)
