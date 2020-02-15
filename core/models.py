from django.db import models
import time
from django.utils import timezone
from django.core.exceptions import ValidationError




def present_or_future_date(value):
    if value < timezone.localdate():
        raise ValidationError("The date cannot be in the past!")
    return value

class Plane(models.Model):
    name = models.CharField(max_length=50,unique=True)
    num_of_seats = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):                           
	    return self.name   


class Flight(models.Model):
    plane_name = models.ForeignKey(Plane,on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField(validators=[present_or_future_date])
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    number_of_seats = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.origin,self.destination)


    
class Cart(models.Model):
    item = models.ForeignKey(Flight, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of flights'

    def get_total(self):
        return self.item.price * self.quantity


class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        
        return total    
              


class Passenger(models.Model):
    flight_id = models.ForeignKey(Flight,null=True,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    GENDER_CHOICES = [('M','Male'),('F','Female')]
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1)

    def __str__(self):
        return self.full_name

      


class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger,on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)

    def __str__(self):
        return '{}  --> ({})'.format(self.passenger,self.flight)

class User_Info(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name