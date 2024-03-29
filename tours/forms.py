from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from tours.models import *

payment_systems = (('Visa', 'Visa'),
                   ('MasterCard', 'MasterCard'),
                   ('МИР', 'МИР'))

class ChoiceInput(forms.Select):
    input_type = 'date'

# class Numberinput(forms.NumberInput):
#     read

class PasswordInput(forms.PasswordInput):
    input_type = "password"

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='*Логин')
    password1 = forms.CharField(label='*Пароль', widget=PasswordInput)
    password2 = forms.CharField(label='*Повтор пароля', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class RegisterClientForm(forms.ModelForm):
    FIO = forms.CharField(label='*ФИО')
    birthday = forms.DateField(label='*дата рождения',
                               widget=forms.DateInput(attrs={'style': 'width : fit-content', 'type': 'date'}),
                               validators=[date_valid_revers])
    email = forms.EmailField(label='*Email')
    phone = forms.CharField(label="Номер телефона", required=False)
    passport_series_number = forms.CharField(label='*Серия/номер паспорта')
    inter_passport_series_number = forms.CharField(label='Серия/номер загран. паспорта', required=False)

    class Meta:
        model = Clients
        fields = ('FIO', 'birthday', 'email', 'phone', 'passport_series_number', 'inter_passport_series_number',)

class BookingForm(forms.ModelForm):
    room = forms.ModelChoiceField(label='Номер', queryset=Rooms.objects.none(), )
    payment = forms.ModelChoiceField(label='Способ оплаты', queryset=Payment.objects.none(), )
    adults_count = forms.IntegerField()
    kids_count = forms.IntegerField()

    client = forms.ModelChoiceField(queryset=Clients.objects.none(), widget=forms.HiddenInput(), required=False)
    tour = forms.ModelChoiceField(queryset=Tours.objects.none(), widget=forms.HiddenInput(), required=False)
    total_price = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    payment_status = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop('hotel', None)
        payment = kwargs.pop('payment', None)
        self.tour_inp = kwargs.pop('tour', None)
        self.client_inp = kwargs.pop('client', None)
        self.bp = self.tour_inp.base_price
        rooms = Rooms.objects.filter(hotel=hotel)

        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['payment'].queryset = payment
        self.fields['room'].queryset = rooms
        self.fields['kids_count'] = forms.IntegerField(max_value=self.tour_inp.max_kids, label='Количество детей',
                                                       min_value=0, initial=0)
        self.fields['adults_count'] = forms.IntegerField(max_value=self.tour_inp.max_adults, label='Количество взрослых',
                                                         min_value=0, initial=0, widget=forms.NumberInput(attrs={'type':'number'}))


    def clean(self):
        clean_data = super().clean()
        c_k = clean_data.get('kids_count')
        c_a = clean_data.get('adults_count')

        if c_a + c_k == 0:
            raise ValidationError('Неверное число клиентов')

    def clean_client(self):
        return self.client_inp

    def clean_tour(self):
        return self.tour_inp

    def clean_total_price(self):
        return self.bp

    def clean_payment_status(self):
        return 'оплачен'

    class Meta:
        model = Booking
        fields = ('room', 'payment', 'adults_count', 'kids_count',  'client', 'tour', 'total_price', 'payment_status')

class PaymentForm(forms.ModelForm):
    payment_system = forms.ChoiceField(choices=payment_systems, label='Платежная система', widget=forms.Select())
    card_number = forms.CharField(label='Номер карты', validators=[car_number_valid])
    card_date = forms.DateField(label='Срок действия',
                                widget=forms.DateInput(attrs={'style': 'width : fit-content', 'type': 'date'}),
                                validators=[date_valid])

    client = forms.ModelChoiceField(queryset=Clients.objects.none(), widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.client_inp = kwargs.pop('client', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
    #
    def clean_client(self):
        return self.client_inp

    class Meta:
        model = Payment
        fields = ('payment_system', 'card_number', 'card_date', 'client')