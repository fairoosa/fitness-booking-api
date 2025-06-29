from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from pytz import timezone

import logging
logger = logging.getLogger(__name__)

from .models import ClassType, FitnessClass, Booking


class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassType
        fields = ['id', 'class_name']


class FitnessClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_type.class_name', read_only=True)
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'class_type', 'class_name', 'instructor', 'start_time', 'end_time', 'available_slots']

    def get_start_time(self, obj):
        return obj.start_time.astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')

    def get_end_time(self, obj):
        return obj.end_time.astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'class_id', 'client_name', 'client_email']

    def validate(self, data):
        class_id = data['class_id']
        client_email = data['client_email']

        if class_id.available_slots <= 0:
            logger.info(f"No available slots for this class id {class_id.id}.")
            raise serializers.ValidationError("No available slots for this class.")

        try:
            validate_email(client_email)
        except DjangoValidationError:
            logger.info(f"Invalid email format: {client_email}")
            raise serializers.ValidationError("Invalid email format.")

        if Booking.objects.filter(class_id=class_id, client_email=client_email).exists():
            logger.info(f"Duplicate booking attempt for email {client_email} in class ID {class_id.id}")
            raise serializers.ValidationError("This email has already booked this class.")

        return data

    def create(self, validated_data):
        class_id = validated_data['class_id']
        class_id.available_slots -= 1
        class_id.save()

        booking = Booking.objects.create(**validated_data)

        logger.info(
            f"Booking created: {booking.client_name} | {booking.client_email} | Class ID: {class_id.id}"
        )

        return booking
