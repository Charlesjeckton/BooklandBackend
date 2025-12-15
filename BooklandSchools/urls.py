from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Optional: Simple API root for testing
@api_view(["GET"])
def api_root(request):
    return Response({
        "message": "Welcome to Bookland Backend API!",
        "endpoints": {
            "admin": "/admin/",
            "app_urls": "/api/ (defined in booklandapp.urls)"
        }
    })


# Optional: Simple root view for browser access
def home(request):
    return JsonResponse({"message": "Bookland Backend is live!"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),  # Root URL now works
    path("api/", include("booklandapp.urls")),  # All app URLs under /api/
    path("api-root/", api_root),  # Optional API test endpoint
]

# Serve media & static files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
