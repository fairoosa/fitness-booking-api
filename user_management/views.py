from django.shortcuts import render
from django.utils import timezone 
from pytz import timezone as pytz_timezone  

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import ClassType, FitnessClass, Booking
from .serializers import ClassTypeSerializer, FitnessClassSerializer, BookingSerializer


class ClassTypeListCreateView(generics.ListCreateAPIView):
    queryset = ClassType.objects.all().order_by('-created_at')
    serializer_class = ClassTypeSerializer


class FitnessClassView(generics.ListCreateAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        ist = pytz_timezone('Asia/Kolkata')
        ist_now = timezone.now().astimezone(ist)
        return FitnessClass.objects.filter(start_time__gt=ist_now).order_by('start_time')

    

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if not email:
            raise ValidationError({"detail": "Email query parameter is required."})
        return Booking.objects.filter(client_email=email).order_by('-created_at')