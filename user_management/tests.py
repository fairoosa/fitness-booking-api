from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from datetime import timedelta

from .models import ClassType, FitnessClass, Booking


class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.class_type = ClassType.objects.create(class_name='Yoga')

        self.fitness_class = FitnessClass.objects.create(
            class_type=self.class_type,
            instructor='Jane Doe',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            available_slots=2
        )

    def test_view_classes(self):
        """Test GET /classes/ returns upcoming classes"""
        response = self.client.get('/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_successful_booking(self):
        """Test POST /book/ creates a new booking"""
        data = {
            'class_id': self.fitness_class.id,
            'client_name': 'John Smith',
            'client_email': 'john@example.com'
        }
        response = self.client.post('/book/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_booking(self):
        """Test that the same user can't book the same class twice"""
        self.client.post('/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'John Smith',
            'client_email': 'john@example.com'
        })
        response = self.client.post('/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'John Smith',
            'client_email': 'john@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already booked", str(response.data).lower())

    def test_overbooking(self):
        """Test that booking fails when no slots are available"""
        for i in range(2):
            self.client.post('/book/', {
                'class_id': self.fitness_class.id,
                'client_name': f'User{i}',
                'client_email': f'user{i}@example.com'
            })
        response = self.client.post('/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'User3',
            'client_email': 'user3@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("no available slots", str(response.data).lower())

    def test_view_bookings_by_email(self):
        """Test GET /bookings/?email= returns bookings for a user"""
        self.client.post('/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'John Smith',
            'client_email': 'john@example.com'
        })
        response = self.client.get('/bookings/?email=john@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_invalid_email_booking(self):
        """Test POST /book/ fails with invalid email format"""
        response = self.client.post('/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'John Smith',
            'client_email': 'invalid-email'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("enter a valid email address", str(response.data).lower())

