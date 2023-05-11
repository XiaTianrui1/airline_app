from django.contrib import admin

# Register your models here.
from .models import Aircraft,Airports,Passengers,PaymentProvider,PassengersBookings,Flight,Bookings,Invoices

admin.site.register(Aircraft)
admin.site.register(Airports)
admin.site.register(Passengers)
admin.site.register(PaymentProvider)
admin.site.register(PassengersBookings)
admin.site.register(Flight)
admin.site.register(Bookings)
admin.site.register(Invoices)