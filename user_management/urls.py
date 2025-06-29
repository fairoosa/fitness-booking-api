from django.urls import path

from .views import ClassTypeListCreateView, FitnessClassView, BookingListCreateView, BookingListView


urlpatterns = [
    path('class-types/', ClassTypeListCreateView.as_view(), name='class-types'),
    path('classes/', FitnessClassView.as_view(), name='classes'),
    path('book/', BookingListCreateView.as_view(), name='book'),
    path('bookings/', BookingListView.as_view(), name='bookings') 
]