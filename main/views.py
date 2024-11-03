import random
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, DeleteView, UpdateView

from main.models import Car, CarModel, Brand  # Добавьте Brand здесь
from .forms import NewModel
from main.filters import CarFilter


def favorites(request):
    # Получаем избранные автомобили для отображения (предполагается, что у вас есть поле или метод для избранного)
    favorite_cars = Car.objects.filter(is_favorite=True)  # Замените is_favorite на соответствующее поле

    context = {
        'favorite_cars': favorite_cars
    }

    return render(request, 'favorites.html', context)

class CarUpdate(UpdateView):
    model = CarModel
    template_name = 'main/newmodel.html'
    form_class = NewModel
    success_url = '/'


class CarDelete(DeleteView):
    model = CarModel
    template_name = 'main/car_delete.html'
    success_url = '/'


def popular(request):
    cars = Car.objects.all()
    car_filter = CarFilter(request.GET, queryset=cars)  # Здесь передаем queryset
    brands = Brand.objects.all()  # Если вам нужно получить список всех брендов

    return render(request, 'main/popular.html', {'filter': car_filter, 'brands': brands, 'cars': cars})

def form_newmodel(request):
    error = ''
    if request.method == 'POST':
        form = NewModel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newcar')
        else:
            error = 'Форма была заполнена неверно'
    form = NewModel()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/favorites.html', data)


def filter_cars(request):
    brand_id = request.GET.get('brand_id')
    model_id = request.GET.get('model_id')
    if brand_id:
        cars = Car.objects.filter(model__brand_id=brand_id)
        if model_id:
            cars = cars.filter(model_id=model_id)
    else:
        cars = Car.objects.all()

    return render(request, 'main/car_list_partial.html', {'cars': cars})
def get_models_by_brand(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse({'models': list(models)})


class CarDetail(DetailView):
    model = Car  # Измените CarModel на Car
    template_name = 'main/car_detail.html'
    context_object_name = 'car'


def toggle_favorite(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        # Находим автомобиль по ID, если не найден, возвращаем 404
        car = get_object_or_404(Car, id=car_id)

        # Переключаем состояние избранного
        car.is_favorite = not car.is_favorite
        car.save()

        # Возвращаем ответ в формате JSON
        return JsonResponse({'is_favorite': car.is_favorite})
def favorites_view(request):
    # Получаем все автомобили, добавленные в избранное
    favorites = Car.objects.filter(is_favorite=True)  # или используйте вашу логику получения избранных
    return render(request, 'main/favorites.html', {'favorites': favorites})