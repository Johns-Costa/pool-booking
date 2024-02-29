from django.shortcuts import get_object_or_404, render, redirect
from .models import Booking, Class
from .forms import BookingForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ValidationError

# Create your views here.

@login_required
def index(request):
    # Exclude canceled classes from the queryset
    classes = Class.objects.filter(canceled=False)
    bookings = Booking.objects.all()
    return render(request, 'booking/index.html', {'classes': classes, 'bookings': bookings})

@login_required
def book_class(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        try:
            form.is_valid()
            # Set the user before saving the form
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Booking successful!')
            return redirect('index')
        except ValidationError as e:
                messages.error(request, str('Cannot book classes in the past.'))
        except ValueError as e:
            messages.error(request, 'Form is not valid. Please check your inputs.')
    else:
        form = BookingForm()

    return render(request, 'booking/booking_form.html', {'form': form})

@staff_member_required
def manage_classes(request):
    classes = Class.objects.all()
    return render(request, 'booking/manage_classes.html', {'classes': classes})

@staff_member_required
def add_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        class_description = request.POST.get('class_description')

        if class_name and class_description:
            Class.objects.create(name=class_name, description=class_description)
            messages.success(request, 'Class added successfully!')
            return redirect('manage_classes')
        else:
            messages.error(request, 'Both class name and description are required.')

    return HttpResponse('Invalid request.')

@staff_member_required
def cancel_class(request, class_id):
    my_class = get_object_or_404(Class, pk=class_id)

    if request.method == 'POST':
        my_class.delete()  # Delete the class permanently
        messages.success(request, 'Class deleted successfully!')
        return redirect('manage_classes')

    return render(request, 'booking/cancel_class.html', {'class': my_class})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the main page after editing
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/edit_booking.html', {'form': form})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        # Implement logic to handle cancellation (e.g., set a 'canceled' flag)
        booking.delete()  # This is just an example; adjust based on your requirements
        return redirect('index')  # Redirect to the main page after cancellation

    return render(request, 'booking/cancel_booking.html', {'booking': booking})