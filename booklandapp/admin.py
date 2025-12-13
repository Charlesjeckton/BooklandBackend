from django.contrib import admin

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

# Register your models here.
admin.site.register(AdmissionMessage)
admin.site.register(EnquiryMessages)
admin.site.register(TestimonialsMessage)
admin.site.register(LeadershipMessage)
admin.site.register(AlumniMessage)
admin.site.register(FeeStructure)
admin.site.register(Event)
admin.site.register(FeaturedEvent)
admin.site.register(GalleryImage)
admin.site.register(KeyAdmissionDeadline)
