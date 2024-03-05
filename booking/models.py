from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Time periods variations
TIME_PERIODS = (
    (0, '9:00-9:45'),
    (1, '10:00-10:45'),
    (2, '11:00-11:45'),
    (3, '14:00-14:45'),
    (4, '15:00-15:45'),
    (5, '16:00-16:45'),
    (6, '17:00-17:45'),
    (7, '18:00-18:45'),
)


class Class(models.Model):
    """
    Represents a class available for booking in the Swimming Pool Booking System.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


def validate_time_period(value):
    if value not in dict(TIME_PERIODS).keys():
        raise ValidationError("Invalid time period")


class Booking(models.Model):
    """
    Represents a user's booking for a specific class in the Swimming Pool Booking System.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.IntegerField(choices=TIME_PERIODS,
                               default=0, validators=[validate_time_period])
    selected_class = models.ForeignKey(Class, on_delete=models.CASCADE,
                                       null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to validate and prevent booking classes in the past.
        """
        # Convert timezone.now() to a date object
        current_date = timezone.now().date()

        # Check if the selected date is in the past
        if self.date < current_date:
            raise ValidationError("Cannot book classes in the past.")

        super().save(*args, **kwargs)
