from django.apps import AppConfig

class BookingConfig(AppConfig):
    """
    Provides primary key type for the booking app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'
