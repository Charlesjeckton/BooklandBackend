import datetime
from django.db import models
from cloudinary.models import CloudinaryField


# =========================
# Admission Messages
# =========================
class AdmissionMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.message}"


# =========================
# Enquiry Messages
# =========================
class EnquiryMessages(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"


# =========================
# Testimonials
# =========================
class TestimonialsMessage(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(blank=True, null=True)  # Cloudinary URL
    title = models.CharField(max_length=50)
    testimonial = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.title}"


# =========================
# Leadership Messages
# =========================
class LeadershipMessage(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    image = models.URLField(blank=True, null=True)  # Cloudinary URL
    designation = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.designation}"


# =========================
# Alumni Messages
# =========================
def current_year():
    return datetime.date.today().year


def year_choices():
    return [(r, r) for r in range(2014, current_year() + 1)]


class AlumniMessage(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(blank=True, null=True)  # Cloudinary URL
    title = models.CharField(max_length=100)
    year_of_completion = models.IntegerField(
        choices=year_choices(),
        default=current_year
    )
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.title}"


# =========================
# Fee Structure
# =========================
class FeeStructure(models.Model):
    LEVEL_CHOICES = [
        ("Play Group", "Play Group"),
        ("PP1 - PP2", "PP1 - PP2"),
        ("Grade 1 - 3", "Grade 1 - 3"),
        ("Grade 4 - 6", "Grade 4 - 6"),
        ("Junior Secondary", "Junior Secondary"),
    ]

    level = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES,
        unique=True,
        help_text="Select the school level for this fee structure"
    )

    tuition_per_term = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Tuition fee per term in KES"
    )

    meals_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Meals fee per term in KES"
    )

    transport_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Transport fee per term in KES (optional)"
    )

    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total approximate fee per term in KES"
    )

    # CloudinaryField for PDF upload
    fee_structure_file = CloudinaryField(
        resource_type='raw',  # 'raw' for PDF files
        folder='fee_structures/',  # Optional folder in Cloudinary
        blank=True,
        null=True,
        help_text="Upload the fee structure PDF (public or private)"
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when record was created
    updated_at = models.DateTimeField(auto_now=True)  # Optional: track when record was updated

    class Meta:
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structures"
        ordering = ['level']  # Orders by level in admin and queries

    def __str__(self):
        return f"{self.level} - Total: KES {self.total_fee}"


# =========================
# Events
# =========================
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Arts', 'Arts'),
        ('Community', 'Community'),
        ('Academic', 'Academic'),
        ('Sports', 'Sports'),
        ('Cultural', 'Cultural'),
        ('Workshops', 'Workshops'),
        ('Conferences', 'Conferences'),
    ]

    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    day = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.month} {self.day}, {self.year}"


# =========================
# Featured Events
# =========================
class FeaturedEvent(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)  # Cloudinary URL
    description = models.TextField()

    class Meta:
        verbose_name = "Featured Event"
        verbose_name_plural = "Featured Events"

    def __str__(self):
        return self.title

    def get_date_range_display(self):
        if self.end_date:
            return f"{self.start_date.strftime('%B %d')} - {self.end_date.strftime('%d, %Y')}"
        return self.start_date.strftime('%B %d, %Y')


# =========================
# Gallery Images
# =========================
class GalleryImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True, null=True)  # Cloudinary URL

    def __str__(self):
        return self.title or "Gallery Image"


# =========================
# Admission Deadlines
# =========================
class KeyAdmissionDeadline(models.Model):
    SEMESTER_CHOICES = [
        ('Term One', 'Term One'),
        ('Term Two', 'Term Two'),
        ('Term Three', 'Term Three'),
        ('Mid-Term One', 'Mid-Term One'),
        ('Mid-Term Two', 'Mid-Term Two'),
    ]

    name = models.CharField(
        max_length=50,
        choices=SEMESTER_CHOICES,
        unique=True,
        help_text="Name of the admission period"
    )
    deadline_date = models.DateField(
        help_text="Deadline date"
    )

    class Meta:
        verbose_name = "Key Admission Deadline"
        verbose_name_plural = "Key Admission Deadlines"
        ordering = ['deadline_date']

    def __str__(self):
        return f"{self.name} - {self.deadline_date.strftime('%B %d, %Y')}"
