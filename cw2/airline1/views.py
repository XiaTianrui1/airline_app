import requests
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import *


# GET
@csrf_exempt
def find_flight(request):
    # req = json.loads(request.body)
    arrival_airport = request.GET.get("arrival_airport")
    departure_airport = request.GET.get("departure_airport")
    date = request.GET.get("date")
    # arrival_airport = req["arrival_airport"]
    # departure_airport = req["departure_airport"]
    # date = req["date"]
    date_list = date.split("/")
    date = date_list[2] + "-" + date_list[1] + "-" + date_list[0]
    if not all([arrival_airport, departure_airport, date]):
        return JsonResponse({"status": 500, "message": "Incomplete flight information!"})
    arrival_airport_object = Airports.objects.get(name=arrival_airport)
    departure_airport_object = Airports.objects.get(name=departure_airport)
    if not all([arrival_airport_object, departure_airport_object]):
        return JsonResponse({"status": 500, "message": "Can not find the airport!"})
    flights = Flight.objects.filter(
        arrival_airport=arrival_airport_object.id,
        departure_airport=departure_airport_object.id,
        date=date
    )
    results = []
    for flight in flights:
        price = str(flight.first_price) + "/" + str(flight.second_price) + "/" + str(flight.third_price)
        result = {
            'flight_id': flight.id,
            'flight_num': flight.flight_num,
            'company_name': 'ceair',
            'arrival_airport': flight.arrival_airport.name,
            'departure_airport': flight.departure_airport.name,
            'departure_datetime': flight.departure_time,
            'arrival_datetime': flight.arrival_time,
            'price': price,
            'remaining_seats': flight.seat_number
        }
        results.append(result)
    if results:
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'message': 'No flights found.'}, status=200, content_type='text/plain')


# GET
@csrf_exempt
def payment_methods(request):
    payment_providers = PaymentProvider.objects.all()
    results = []
    for payment_provider in payment_providers:
        result = {
            'payment_provider_name': payment_provider.name,
        }
        results.append(result)
    if results:
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'message': 'No payment provider found.'}, status=200, content_type='text/plain')


# POST
@csrf_exempt
def bookflight(request):
    req = json.loads(request.body)
    flight_num = req["flight_num"]
    passenger = req["passenger"]
    seat_num = req["seats_num"]
    seat_class = req["seats_class"]
    if not all([flight_num, passenger, seat_num, seat_class]):
        return JsonResponse({"status": 500, "message": "Incomplete booking information!"})
    else:
        if len(passenger) != seat_num:
            return JsonResponse({"status": 200, "message": "Seat number and passengers number are not the same!"})
        else:
            flight = Flight.objects.get(flight_num=flight_num)
            if flight.remaining_seats >= seat_num:
                if seat_class == 'Economy':
                    if flight.remaining_third_seats >= seat_num:
                        single_price = flight.third_price
                        flight.remaining_third_seats = flight.remaining_third_seats - seat_num
                        flight.remaining_seats = flight.remaining_seats - seat_num
                        flight.save()
                    else:
                        return JsonResponse({'message': 'There is no remaining economy class for this flight!'},
                                            status=200,
                                            content_type='text/plain')
                if seat_class == 'Business':
                    if flight.remaining_second_seats >= seat_num:
                        single_price = flight.second_price
                        flight.remaining_second_seats = flight.remaining_second_seats - seat_num
                        flight.remaining_seats = flight.remaining_seats - seat_num
                        flight.save()
                    else:
                        return JsonResponse({'message': 'There is no remaining business class for this flight!'},
                                            status=200,
                                            content_type='text/plain')
                if seat_class == 'First':
                    if flight.remaining_first_seats >= seat_num:
                        single_price = flight.first_price
                        flight.remaining_first_seats = flight.remaining_first_seats - seat_num
                        flight.remaining_seats = flight.remaining_seats - seat_num
                        flight.save()
                    else:
                        return JsonResponse({'message': 'There is no remaining first class for this flight!'},
                                            status=200,
                                            content_type='text/plain')
                total_price = seat_num * single_price
                booking_num = uuid.uuid1()
                booking = Bookings(booking_num=booking_num, flight_id=flight, num_ticket=seat_num, price=total_price,
                                   booking_datetime=datetime.now(),
                                   status="ON_HOLD", seat_class=seat_class)
                booking.save()
                flight.seat_number = flight.seat_number - 1
                flight.save()
                for item in passenger:
                    exist_passenger = Passengers.objects.filter(passport_num=item[0])
                    print(exist_passenger)
                    if not exist_passenger:
                        add_passenger = Passengers(passport_num=item[0], name=item[1], gender=item[2],
                                                   nationality=item[3])
                        add_passenger.save()
                        add_passengersbookings = PassengersBookings(passengers_id=add_passenger, booking_id=booking)
                        add_passengersbookings.save()
                    else:
                        add_passengersbookings = PassengersBookings(passengers_id=exist_passenger[0],
                                                                    booking_id=booking)
                        add_passengersbookings.save()
                return JsonResponse({"booking_num": booking_num, "booking_status": booking.status,
                                     "total_price": total_price}, status=200, content_type='text/plain')
            else:
                return JsonResponse({'message': 'There is no remaining seat for this flight!'}, status=200,
                                    content_type='text/plain')


# POST
@csrf_exempt
def payforbooking(request):
    req = json.loads(request.body)
    booking_number = req["booking_number"]
    payment_provider_name = req["payment_provider_name"]
    payment_provider_object = PaymentProvider.objects.filter(name=payment_provider_name)
    if payment_provider_object:
        payment_provider_id = payment_provider_object[0].id
        booking = Bookings.objects.filter(booking_num=booking_number)
        if booking:
            price = booking[0].price
            airline_login_name = payment_provider_object[0].airline_login_name
            if not all([booking_number, payment_provider_id, price, airline_login_name]):
                return JsonResponse({"status": 500, "message": "Incomplete payment information!"})
            else:
                if payment_provider_name == "PayPal":
                    url = 'http://arinnnnnn.pythonanywhere.com/createinvoice/'
                elif payment_provider_name == "WeChat Pay":
                    url = 'http://sc19jz2.pythonanywhere.com/createinvoice/'
                elif payment_provider_name == "Alipay":
                    url = 'http://sc19wc.pythonanywhere.com/createinvoice/'
                elif payment_provider_name == "Apple Pay":
                    url = 'http://arinnnnnn.pythonanywhere.com/createinvoice/'
                else:
                    return JsonResponse({'message': 'No Provider Found.'}, status=500, content_type='text/plain')
                res = requests.post(url, json={"booking_number": booking_number,
                                               "payment_provider_name": payment_provider_name,
                                               "amount": price, "receiver_account_number": airline_login_name})
                res = res.json()
                invoice_num = res["invoice_num"]
                stamp = res["stamp"]
                create_time = res["create_time"]
                invoice = Invoices(invoice_num=invoice_num, booking_id=booking[0], status=booking[0].status,
                                   date_time=create_time,
                                   stamp=stamp, payment_provider_id=payment_provider_object[0])
                invoice.save()
                return JsonResponse({"invoice_num": invoice_num, "booking_status": booking[0].status,
                                     "price": price, "datetime": invoice.date_time, "booking_num": booking_number,
                                     "payment_provider_name": payment_provider_object[0].name}, status=200,
                                    content_type='text/plain')
        else:
            return JsonResponse({'message': 'No booking found.'}, status=200, content_type='text/plain')
    else:
        return JsonResponse({'message': 'No payment provider found.'}, status=200, content_type='text/plain')


# GET
@csrf_exempt
def bookingstatus(request):
    # req = json.loads(request.body)
    booking_number = request.GET.get("booking_number")
    # booking_number = req["booking_number"]
    if not booking_number:
        return JsonResponse({"status": 500, "message": "Incomplete booking information!"})
    booking = Bookings.objects.filter(
        booking_num=booking_number
    )
    status = booking[0].status
    if booking:
        return JsonResponse(
            {"booking_status": status, "booking_num": booking[0].booking_num,
             "flight_num": booking[0].flight_id.flight_num,
             "booking_datetime": booking[0].booking_datetime, "price": booking[0].price}, safe=False)
    else:
        return JsonResponse({'message': 'No booking found.'}, status=200, content_type='text/plain')


# GET
@csrf_exempt
def cancelbooking(request):
    # req = json.loads(request.body)
    booking_number = request.GET.get("booking_number")
    # booking_number = req["booking_number"]
    if not booking_number:
        return JsonResponse({"status": 200, "message": "Incomplete booking information!"})
    booking = Bookings.objects.filter(
        booking_num=booking_number
    )
    if booking:
        booking[0].status = 'CANCELLED'
        booking[0].save()
        return JsonResponse({"booking_status": "CANCELLED", "booking_num": booking_number}, safe=False)
    else:
        return JsonResponse({'message': 'No booking found.'}, status=200, content_type='text/plain')


# POST
@csrf_exempt
def finalizebooking(request):
    res = json.loads(request.body)
    booking_num = res["booking_num"]
    stamp = res["stamp"]
    invoice_num = res["invoice_num"]
    if not all([booking_num, stamp, invoice_num]):
        return JsonResponse({"status": 200, "message": "Incomplete payment information!"})
    else:
        airline_invoice = Invoices.objects.filter(invoice_num=invoice_num)
        if airline_invoice:
            airline_booking = Bookings.objects.filter(booking_num=booking_num)
            if airline_booking:
                if airline_invoice[0].stamp == stamp:
                    airline_invoice[0].status = "PAID"
                    airline_booking[0].status = "FINISHED"
                    airline_invoice[0].save()
                    airline_booking[0].save()
                    return JsonResponse({"booking_num": booking_num, "booking_status": airline_booking[0].status}, status=200,
                                        content_type='text/plain')
                else:
                    return JsonResponse({"message": "Wrong stamp."}, status=200, content_type='text/plain')
            else:
                return JsonResponse({'message': 'No matching booking found.'}, status=200, content_type='text/plain')
        else:
            return JsonResponse({'message': 'No matching invoice found.'}, status=200, content_type='text/plain')
