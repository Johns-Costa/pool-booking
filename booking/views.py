from django.shortcuts import render, redirect
from .models import Booking, Class
from .forms import BookingForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def index(request):
    classes = Class.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'booking/index.html', {'classes': classes, 'bookings': bookings})

def book_class(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            if not Booking.objects.filter(date_time=form.cleaned_data['date_time']).exists():
                form.save()
                messages.success(request, 'Booking successful!')
                return redirect('index')
            else:
                messages.error(request, 'This class is already booked. Please choose another time.')
    else:
        form = BookingForm()

    return render(request, 'booking/booking_form.html', {'form': form})

@staff_member_required
def manage_classes(request):
    classes = Class.objects.all()
    return render(request, 'booking/manage_classes.html', {'classes': classes})
