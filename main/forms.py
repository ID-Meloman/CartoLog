from django.forms import ModelForm, TextInput, SelectMultiple, NumberInput, ClearableFileInput, Select, EmailInput, \
    PasswordInput
from django import forms
from .models import Car, CarModel, Person


class NewCar(ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'color']

        widgets = {
            'model': SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Модель',
            }),
            'color': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цвет'
            })
        }


class NewModel(ModelForm):
    class Meta:
        model = CarModel
        fields = ['brand', 'name']
        widgets = {
            'brand': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Марка'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Модель'
            })
        }


class NewPerson(ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'password']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'required': True
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта',
                'required': True
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'required': True,
                'autocomplete': 'new-password'
            })
        }


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}),
        label="Почта пользователя"
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label="Пароль"
    )



