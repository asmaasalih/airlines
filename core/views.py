from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.db.models import Q
from .models import Plane, Flight, Ticket, Passenger, Cart, Order, User_Info
from .forms import SearchForm, PassengerForm, UserInfoForm

class HomePageView(TemplateView):
	template_name = 'core/home.html'

	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		context['form'] = SearchForm()
		return context


class SearchResultView(ListView):
	model = Flight 
	template_name = 'core/flight_list.html'
	context_object_name = 'flight'

	def get_queryset(self):
		departure  = self.request.GET.get('origin')
		arrival  = self.request.GET.get('destination')
		departure_date  = self.request.GET.get('departure_date')
		if departure_date:
			object_list = Flight.objects.filter(
					Q(origin__exact=departure) 
					& Q(destination__exact=arrival) 
					& Q(date__contains=departure_date) 
			)	
			return object_list

	def get_context_data(self, *args, **kwargs):
		context = super(SearchResultView,self).get_context_data(*args, **kwargs)
		departure  = self.request.GET.get('origin')
		arrival  = self.request.GET.get('destination')
		return_date = self.request.GET.get('return_date',None)
		context['flight'] = Flight
		if return_date:
			context['return_list'] = Flight.objects.filter(
					Q(origin__exact=arrival) 
					& Q(destination__exact=departure) 
					& Q(date__contains=return_date) 
				)
		return context


class FlightDetailView(DetailView):
	model = Flight
	template_name = 'core/flight_detail.html'
	context_object_name = 'flight'
	
	def get_context_data(self, **kwargs):
		context = super(FlightDetailView, self).get_context_data(**kwargs)
		context['form1'] = UserInfoForm()
		context['form2'] = PassengerForm()
		return context

	def post(self,request,*args,**kwargs):
		form1 = UserInfoForm(request.POST)
		form2 = PassengerForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()		
		return redirect('/')


def add_to_cart(request, flight_id):
    item = get_object_or_404(Flight, id=flight_id)
    order_item, created = Cart.objects.get_or_create(item=item)
    order_qs = Order.objects.filter(ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("cart_home")
        else:
            order.orderitems.add(order_item)
            return redirect("cart_home")
    else:
        order = Order.objects.create()
        order.orderitems.add(order_item)
        return redirect("cart_home")


def remove_from_cart(request, flight_id):
	item = get_object_or_404(Flight, id=flight_id)
	cart_qs = Cart.objects.filter(item=item)
	if cart_qs.exists():
		cart = cart_qs[0]
		if cart.quantity > 1:
			cart.quantity -= 1
			cart.save()
		else:
			cart_qs.delete()		
	order_qs = Order.objects.filter(ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.orderitems.filter(item__id=item.id).exists():
			order_item = Cart.objects.filter(item=item)[0]
			order.orderitems.remove(order_item)
			return redirect("cart_home")
		else:
			return redirect("cart_home")
	else:
		return redirect("cart_home")		


def CartView(request):
    carts = Cart.objects.all()
    orders = Order.objects.filter(ordered=False)
    if carts.exists():
        order = orders[0]
        return render(request, 'core/cart.html', {"carts": carts, 'order': order})	
    else:
        return redirect("cart_home")


def decreaseCart(request, flight_id):
	item = get_object_or_404(Flight, id=flight_id)
	order_qs = Order.objects.filter(ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.orderitems.filter(item__id=item.id).exists():
			order_item = Cart.objects.filter(item=item)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()	
			else:
				order.orderitems.remove(order_item)
				order_item.delete()
			return redirect("cart_home")
		else:
			return redirect("cart_home")
	else:
		return redirect("cart_home")
