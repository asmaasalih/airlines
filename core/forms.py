from django import forms
from .models import Passenger, User_Info


class SearchForm(forms.Form):
    CHOICES = [(i,str(i)) for i in range(1,21)]
    one_way        = forms.BooleanField(widget=forms. CheckboxInput(attrs={'id' :'one-way','onclick':'IsOneWay();','defaultValue':False}),required=False)
    origin         = forms.CharField(label='From',max_length=100)
    destination    = forms.CharField(label='To',max_length=100)
    departure_date = forms.DateField(label='',widget=forms.DateInput(attrs={'type': 'date'}))
    return_date    = forms.DateField(label='',widget=forms.DateInput(attrs={'type': 'date','id' :'return-date'}))
    seats        = forms.TypedChoiceField(choices=CHOICES,coerce=int)


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = '__all__'
        #exclude = ['flight_id']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User_Info
        fields = '__all__'
