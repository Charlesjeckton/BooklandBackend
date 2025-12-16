from django import forms
import cloudinary.uploader
from .models import (
    AdmissionMessage,
    EnquiryMessages,
    TestimonialsMessage,
    LeadershipMessage,
    AlumniMessage,
)


# =========================
# Admission Form
# =========================
class AdmissionMessageForm(forms.ModelForm):
    class Meta:
        model = AdmissionMessage
        fields = ["name", "email", "phone", "message"]


# =========================
# Enquiry Form
# =========================
class EnquiryMessagesForm(forms.ModelForm):
    class Meta:
        model = EnquiryMessages
        fields = ["name", "email", "subject", "message"]


# =========================
# Testimonials Form
# =========================
class TestimonialsMessageForm(forms.ModelForm):
    upload_image = forms.ImageField(required=False, label="Upload Image")

    class Meta:
        model = TestimonialsMessage
        fields = ["name", "title", "testimonial", "upload_image"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("upload_image")
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="bookland/testimonials",
                quality="auto",
                fetch_format="auto",
            )
            instance.image = upload_result["secure_url"]
        if commit:
            instance.save()
        return instance


# =========================
# Leadership Form
# =========================
class LeadershipMessageForm(forms.ModelForm):
    upload_image = forms.ImageField(required=False, label="Upload Image")

    class Meta:
        model = LeadershipMessage
        fields = ["salutation", "name", "designation", "message", "upload_image"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("upload_image")
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="bookland/leadership",
                quality="auto",
                fetch_format="auto",
            )
            instance.image = upload_result["secure_url"]
        if commit:
            instance.save()
        return instance


# =========================
# Alumni Form
# =========================
class AlumniMessageForm(forms.ModelForm):
    upload_image = forms.ImageField(required=False, label="Upload Image")

    class Meta:
        model = AlumniMessage
        fields = ["name", "title", "year_of_completion", "message", "upload_image"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("upload_image")
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="bookland/alumni",
                quality="auto",
                fetch_format="auto",
            )
            instance.image = upload_result["secure_url"]
        if commit:
            instance.save()
        return instance
