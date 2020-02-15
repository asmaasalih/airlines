from django.urls import path
from django.conf.urls import url
from .views import HomePageView,SearchResultView, FlightDetailView, add_to_cart, remove_from_cart, CartView, decreaseCart

#app_name = 'core'

urlpatterns = [
    path('<int:pk>/',FlightDetailView.as_view(),name='flight_detail'),
    path('search_results/',SearchResultView.as_view(),name="search_results"),
    path('',HomePageView.as_view(),name="home"),
    path('cart-add/<flight_id>/', add_to_cart, name='cart-add'),
    path('decrease_cart/<flight_id>/',decreaseCart,name='decrease-cart'),
    path('cart-remove/<flight_id>/', remove_from_cart, name='cart-remove'),
    path('cart_home/',CartView,name='cart_home'),
   
]