from django.db import models
from datetime import datetime


class Airports(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=20)
    time_zone = models.CharField(max_length=20)


class Aircraft(models.Model):
    type = models.CharField(max_length=20)
    tail_number = models.CharField(max_length=20, unique=True)
    seats_number = models.IntegerField(default=100)


class Flight(models.Model):
    flight_num = models.CharField(max_length=255, unique=True)
    aircraft = models.ForeignKey(to=Aircraft, on_delete=models.CASCADE, default='')
    departure_time = models.DateTimeField(default=datetime.now)
    arrival_time = models.DateTimeField(default=datetime.now)
    date = models.DateField(default=datetime(2023, 5, 12, 00, 00, 00, 00).date())
    departure_airport = models.ForeignKey(to=Airports, related_name='departing_flights', on_delete=models.CASCADE,
                                          default='')
    arrival_airport = models.ForeignKey(to=Airports, related_name='arriving_flights', on_delete=models.CASCADE,
                                        default='')
    price = models.IntegerField()
    airline_company = models.CharField(max_length=255, default='ceair')
    first_price = models.IntegerField(default=100)
    second_price = models.IntegerField(default=100)
    third_price = models.IntegerField(default=100)
    first_class_capcity = models.IntegerField(default=100)
    second_class_capcity = models.IntegerField(default=100)
    third_class_capcity = models.IntegerField(default=100)
    seat_number = models.IntegerField(default=100)
    remaining_seats = models.IntegerField(default=100)
    remaining_first_seats = models.IntegerField(default=1)
    remaining_second_seats = models.IntegerField(default=30)
    remaining_third_seats = models.IntegerField(default=100)


class Passengers(models.Model):
    passport_num = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, default="Male")
    nationality = models.CharField(max_length=20)
    email = models.CharField(max_length=30, default="123@qq.com")


class Bookings(models.Model):
    booking_num = models.CharField(max_length=20, unique=True)
    flight_id = models.ForeignKey('Flight', on_delete=models.CASCADE, default='')
    num_ticket = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(max_length=20)
    seat_class = models.CharField(max_length=20, default='Business')
    booking_datetime = models.DateTimeField(default=datetime.now)


class PassengersBookings(models.Model):
    passengers_id = models.ForeignKey('Passengers', on_delete=models.CASCADE, default='')
    booking_id = models.ForeignKey('Bookings', on_delete=models.CASCADE, default='')


class PaymentProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    web_address = models.CharField(max_length=100)
    airline_login_name = models.CharField(max_length=100)
    airline_login_password = models.CharField(max_length=100)


class Invoices(models.Model):
    invoice_num = models.CharField(max_length=20, unique=True)
    booking_id = models.ForeignKey('Bookings', on_delete=models.CASCADE, default='')
    payment_provider_id = models.ForeignKey(to=PaymentProvider, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    date_time = models.DateTimeField()
    stamp = models.CharField(max_length=20)
