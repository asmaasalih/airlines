from django.contrib import admin
from .models import Plane, Flight, Cart, Order, Passenger,Ticket, User_Info


class PlaneAdmin(admin.ModelAdmin):
    list_displayed = ['name', 'number_of_seats']

class FlightAdmin(admin.ModelAdmin):
    list_displayed = ['origin','destination','date']

admin.site.register(Plane,PlaneAdmin)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(User_Info)
admin.site.register(Passenger)
admin.site.register(Ticket)
