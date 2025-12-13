from django import forms
from .models import (
    AdmissionMessage,
    EnquiryMessages,
    TestimonialsMessage,
    LeadershipMessage,
    AlumniMessage,
)


class AdmissionMessageForm(forms.ModelForm):
    class Meta:
        model = AdmissionMessage
        fields = ["name", "email", "phone", "message"]


class EnquiryMessagesForm(forms.ModelForm):
    class Meta:
        model = EnquiryMessages
        fields = ["name", "email", "subject", "message"]


class TestimonialsMessageForm(forms.ModelForm):
    class Meta:
        model = TestimonialsMessage
        fields = ["name", "image", "title", "testimonial"]


class LeadershipMessageForm(forms.ModelForm):
    class Meta:
        model = LeadershipMessage
        fields = ["name", "image", "designation", "message"]


class AlumniMessageForm(forms.ModelForm):
    class Meta:
        model = AlumniMessage
        fields = ["name", "image", "title", "message"]
