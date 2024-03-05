from django.urls import path
from .views import index, book_class, manage_classes, add_class, cancel_class, edit_booking, cancel_booking


urlpatterns = [
    path('', index, name='index'),
    path('book/', book_class, name='book_class'),
    path('manage/', manage_classes, name='manage_classes'),
    path('add_class/', add_class, name='add_class'),
    path('cancel_class/<int:class_id>/', cancel_class, name='cancel_class'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking')   
]
