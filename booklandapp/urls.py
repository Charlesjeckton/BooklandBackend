from django.urls import path
from .views import (
    api_home,
    api_testimonials,
    api_leadership,
    api_gallery,
    api_fees,
    api_events,
    api_featured_events,
    api_alumni,
    api_admission_deadlines,
    api_admissions,
    api_contact,
)

urlpatterns = [
    # -------------------------------------------------
    # API ROOT / HEALTH CHECK
    # -------------------------------------------------
    path("api/", api_home, name="api_home"),

    # -------------------------------------------------
    # READ APIs (GET)
    # -------------------------------------------------
    path("api/testimonials/", api_testimonials, name="api_testimonials"),
    path("api/leadership/", api_leadership, name="api_leadership"),
    path("api/gallery/", api_gallery, name="api_gallery"),
    path("api/fees/", api_fees, name="api_fees"),
    path("api/events/", api_events, name="api_events"),
    path("api/featured-events/", api_featured_events, name="api_featured_events"),
    path("api/alumni/", api_alumni, name="api_alumni"),
    path("api/admission-deadlines/", api_admission_deadlines, name="api_admission_deadlines"),

    # -------------------------------------------------
    # WRITE APIs (POST)
    # -------------------------------------------------
    path("api/admissions/submit/", api_admissions, name="api_admissions"),
    path("api/contact/submit/", api_contact, name="api_contact"),
]
