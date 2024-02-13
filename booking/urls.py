from django.urls import path
from .views import index, book_class, manage_classes

urlpatterns = [
    path('', index, name='index'),
    path('book/', book_class, name='book_class'),
    path('manage/', manage_classes, name='manage_classes'),
]