from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, DeleteView, UpdateView

from main.models import Car, CarModel
from .forms import NewCar, NewModel


# Create your views here.

class CarDetail(DetailView):
    model = CarModel
    template_name = 'main/car_detail.html'
    context_object_name = 'article'

class CarUpdate(UpdateView):
    model = CarModel
    template_name = 'main/newmodel.html'
    form_class = NewModel
    success_url = '/'

class CarDelete(DeleteView):
    model = CarModel
    template_name = 'main/car_delete.html'
    success_url ='/'



def popular(request):
    cars = Car.objects.order_by('-pk')
    print(cars)
    return render(request, 'main/popular.html', {'cars': cars})


def form_newcar(request):
    error = ''
    if request.method == 'POST':
        form = NewCar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('popular_page')
        else:
            error = 'форма была заполнена не верно'
    form = NewCar()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/newcar.html', data)

def form_newmodel(request):
    error = ''
    if request.method == 'POST':
        form = NewModel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newcar')
        else:
            error = 'форма была заполнена не верно'
    form = NewModel()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/newcar.html', data)
