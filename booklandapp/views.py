import calendar
from datetime import date
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib import messages

from BooklandBackend.booklandapp.models import AdmissionMessage, EnquiryMessages, TestimonialsMessage, LeadershipMessage, GalleryImage
from BooklandBackend.booklandapp.models import FeeStructure, Event, AlumniMessage, FeaturedEvent, KeyAdmissionDeadline


# Create your views here.


def index(request):
    testimonials_list = TestimonialsMessage.objects.all()

    # Define months and categories for dropdowns
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    categories = ['Academic', 'Arts', 'Sports', 'Community', 'Cultural', 'Workshops', 'Conferences']

    # Get filter values from GET parameters
    selected_month = request.GET.get('month')
    selected_category = request.GET.get('category')

    # Start with all events
    events_qs = Event.objects.all()

    # Apply filters if selected
    if selected_month:
        events_qs = events_qs.filter(month=selected_month)
    if selected_category:
        events_qs = events_qs.filter(category=selected_category)

    # Sort and limit to latest 4
    events_list = events_qs.order_by('-year', 'month', 'day')[:4]

    context = {
        'testimonials': testimonials_list,
        'events': events_list,
        'months': months,
        'categories': categories,
        'selected_month': selected_month,
        'selected_category': selected_category,
    }
    return render(request, 'index.html', context)


def about(request):
    leadership_team = LeadershipMessage.objects.all()
    gallery_images = GalleryImage.objects.all()  # fetch gallery images from database

    context = {
        'leadership_team': leadership_team,
        'gallery_images': gallery_images,  # include in context
    }

    return render(request, 'about.html', context)


def admissions(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')

        if not name or not email or not message_text:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('admissions')

        AdmissionMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )
        messages.success(request, 'Your request has been submitted successfully!')
        return redirect('admissions')

    deadlines = KeyAdmissionDeadline.objects.all()
    return render(request, 'admissions.html', {'deadlines': deadlines})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        EnquiryMessages.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        return redirect('admission_success')

    return render(request, 'contact.html')


def alumni(request):
    alumni_list = AlumniMessage.objects.all()
    context = {
        'alumni_list': alumni_list
    }
    return render(request, 'alumni.html', context)


def events(request):
    # Get all events ordered chronologically
    event_list = Event.objects.order_by('year', 'month', 'day', 'start_time')

    # Get requested month/year from query parameters, else default to current month
    today = date.today()
    month = request.GET.get('month')
    year = request.GET.get('year')

    if month and year:
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            month = today.month
            year = today.year
    else:
        month = today.month
        year = today.year

    # Ensure month is valid (1-12)
    if not 1 <= month <= 12:
        month = today.month
        year = today.year

    # Compute month name
    month_name = calendar.month_name[month]

    # Compute previous and next month/year
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # Filter events for the displayed month
    month_events = Event.objects.filter(month=month_name, year=year)
    event_days = set(e.day for e in month_events)

    # Generate calendar matrix (weeks × days)
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)

    # Get featured events (can be limited or filtered if needed)
    featured_events = FeaturedEvent.objects.all().order_by('-start_date')[:1]

    # -------------------------------
    # ✅ NEW CODE: count upcoming events per category
    # -------------------------------
    # Define list of month names for easier comparison
    month_names = list(calendar.month_name)

    # Find upcoming events from today forward
    upcoming_events = Event.objects.filter(
        Q(year__gt=today.year) |
        Q(year=today.year,
          month__in=month_names[today.month:]) |
        Q(year=today.year,
          month=month_names[today.month],
          day__gte=today.day)
    )

    # Group by category
    category_counts_query = (
        upcoming_events
        .values('category')
        .annotate(count=Count('id'))
        .order_by('category')
    )

    # Convert to a dictionary for easy template use
    category_counts = {item['category']: item['count'] for item in category_counts_query}

    context = {
        'events': event_list,
        'year': year,
        'month': month,
        'month_name': month_name,
        'month_days': month_days,
        'event_days': event_days,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'featured_events': featured_events,
        'category_counts': category_counts,  # ✅ add to context
    }

    return render(request, 'events.html', context)


def faqs(request):
    return render(request, 'faqs.html')


def fees(request):
    fee_list = FeeStructure.objects.all()
    return render(request, 'fees.html', {'fees': fee_list})
