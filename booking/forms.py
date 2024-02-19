from django import forms
from .models import Booking, Class

class BookingForm(forms.ModelForm):
    selected_class = forms.ModelChoiceField(queryset=Class.objects.all())

    class Meta:
        model = Booking
        fields = ['selected_class', 'date_time', 'user', 'description'] 