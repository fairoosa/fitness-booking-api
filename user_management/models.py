from django.db import models
from django.utils import timezone



class ClassType(models.Model):
    class_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name


class FitnessClass(models.Model):
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE, related_name='fitness_classes')
    instructor = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    available_slots = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_upcoming(self):
        return self.start_time > timezone.now()

    def __str__(self):
        return f"{self.class_type.class_name} with {self.instructor} at {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Booking(models.Model):
    class_id = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} booked {self.class_id}"