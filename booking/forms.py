from django import forms
from .models import Booking, Class  # Import both Booking and Class models

class BookingForm(forms.ModelForm):
    selected_class = forms.ModelChoiceField(queryset=Class.objects.all())  # Move queryset definition here

    class Meta:
        model = Booking
        fields = ['description', 'date_time', 'selected_class']