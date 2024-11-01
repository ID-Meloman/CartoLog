from django.db.models import Model
from django.forms import ModelForm, TextInput, SelectMultiple, NumberInput, ClearableFileInput, Select

from .models import Car, CarModel

class NewCar(ModelForm):
    class Meta:
        model = Car
        fields = ['model','color']

        widgets = {
            'model':SelectMultiple(attrs={
                'class':'form-control',
                'placeholder': 'Модель',
            }),
            'color':TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цвет'
            })
        }

class NewModel(ModelForm):
    class Meta:
        model = CarModel
        fields=['brand', 'name']
        widgets = {
            'brand':Select(attrs={
                'class': 'form-control',
                'placeholder': 'Марка'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Модель'
            })
        }