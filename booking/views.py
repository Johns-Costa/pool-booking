from django.shortcuts import get_object_or_404, render, redirect
from .models import Booking, Class
from .forms import BookingForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your views here.

from django.shortcuts import render
from django.utils import timezone


@login_required
def index(request):
    """
    Displays available and booked classes for the logged-in user.

    **Context**

    ``classes``
        All available classes excluding canceled ones.
    ``bookings``
        Bookings made by the logged-in user.
    ``current_datetime``
        Current date and time.

    **Template:**

    :template:`booking/index.html`
    """
    # Exclude canceled classes from the queryset
    classes = Class.objects.filter(canceled=False)

    # Get bookings for the currently logged-in user
    bookings = Booking.objects.filter(user=request.user)

    # Order bookings by date and time
    bookings = bookings.order_by('date')

    # Get the current datetime
    current_datetime = timezone.now().date()

    context = {
        'classes': classes,
        'bookings': bookings,
        'current_datetime': current_datetime,
    }

    return render(request, 'booking/index.html', context)


@login_required
def book_class(request):
    """
    Handles the booking form submission and displays booking-related messages.

    **Context**

    ``form``
        An instance of :form:`booking.BookingForm`.

    **Template:**

    :template:`booking/booking_form.html`
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        try:
            form.is_valid()
            # Set the user before saving the form
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Booking successful!',
                             extra_tags='booking_form')
            return redirect('book_class')
        except ValidationError:
            messages.error(request, 'Cannot book classes in the past.',
                           extra_tags='booking_form')
        except ValueError:
            messages.error(request,
                           'Form is not valid. Please check your inputs.',
                           extra_tags='booking_form')
    else:
        form = BookingForm()

    return render(request, 'booking/booking_form.html', {'form': form})


@staff_member_required
def manage_classes(request):
    """
    Displays all classes and their bookings for staff members.

    **Context**

    ``classes``
        All available classes.
    ``bookings``
        All bookings for available classes.
    ``current_datetime``
        Current date.

    **Template:**

    :template:`booking/manage_classes.html`
    """
    classes = Class.objects.all()
    # Get the current datetime
    current_datetime = timezone.now().date()

    bookings = Booking.objects.filter(date__gte=current_datetime)

    # Order bookings by date and time
    bookings = bookings.order_by('date')

    context = {
        'classes': classes,
        'bookings': bookings,
        'current_datetime': current_datetime,
    }

    return render(request, 'booking/manage_classes.html', context)


@staff_member_required
def add_class(request):
    """
    Handles the addition of a new class by staff members.

    **Template:**

    Redirects to the 'manage_classes' view on success.
    """
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        class_description = request.POST.get('class_description')

        if class_name and class_description:
            Class.objects.create(name=class_name,
                                 description=class_description)
            messages.success(request, 'Class added successfully!',
                             extra_tags='manage_classes')
            return redirect('manage_classes')
        else:
            messages.error(request,
                           'Both class name and description are required.',
                           extra_tags='manage_classes')

    return HttpResponse('Invalid request.')


@staff_member_required
def cancel_class(request, class_id):
    """
    Handles the cancellation of a class by staff members.

    **Context**

    ``class``
        The class to be canceled.

    **Template:**

    :template:`booking/cancel_class.html`
    """
    my_class = get_object_or_404(Class, pk=class_id)

    if request.method == 'POST':
        my_class.delete()  # Delete the class permanently
        messages.success(request, 'Class deleted successfully!',
                         extra_tags='cancel_class')
        return redirect('manage_classes')

    return render(request, 'booking/cancel_class.html', {'class': my_class})


@login_required
def edit_booking(request, booking_id):
    """
    Allows a logged-in user to edit a booking.

    **Context**

    ``booking``
        An instance of :model:`booking.Booking` to be edited.
    ``form``
        An instance of :form:`booking.BookingForm` populated with existing booking data.

    **Template:**

    :template:`booking/edit_booking.html`
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking edited successfully!',
                             extra_tags='edit_booking')
            return redirect('index')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/edit_booking.html', {'form': form})


@login_required
def cancel_booking(request, booking_id):
    """
    Allows a logged-in user to cancel a booking.

    **Context**

    ``booking``
        An instance of :model:`booking.Booking` to be canceled.

    **Template:**

    :template:`booking/cancel_booking.html`
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!',
                         extra_tags='cancel_booking')
        return redirect('index')

    return render(request, 'booking/cancel_booking.html',
                  {'booking': booking})
