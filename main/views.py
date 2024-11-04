from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView, DeleteView, UpdateView
from main.models import Car, CarModel, Brand, Person, TransmissionDrive
from .forms import NewModel, NewPerson, LoginForm
from main.filters import CarFilter


def info_user(request):
    # Проверяем, авторизован ли пользователь
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_user')

    # Если пользователь авторизован, получаем его данные из базы
    try:
        user = Person.objects.get(id=user_id)
    except Person.DoesNotExist:
        # Если пользователь с таким ID не найден, удаляем данные из сессии и перенаправляем на login_user
        request.session.flush()
        messages.error(request, 'Сессия недействительна, пожалуйста, авторизуйтесь снова.')
        return redirect('login_user')

    # Передаём данные пользователя в шаблон info_user.html
    return render(request, 'authorization/info_user.html', {'user': user})


def logout_user(request):
    # Удаляем данные пользователя из сессии
    request.session.flush()

    # Перенаправляем на страницу входа (или другую страницу по выбору)
    return redirect('popular_page')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                # Ищем пользователя по email
                user = Person.objects.get(email=email)

                # Проверяем пароль
                if user.password == password:
                    # Сохраняем пользователя в сессии
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('popular_page')
                else:
                    messages.error(request, 'Неверный пароль')
            except Person.DoesNotExist:
                messages.error(request, 'Пользователь с такой почтой не найден')
    else:
        form = LoginForm()

    return render(request, 'authorization/login_user.html', {'form': form})


def registration_user_form(request):
    error = ''
    if request.method == 'POST':
        form = NewPerson(request.POST)
        if form.is_valid():
            form.save()
            return redirect('popular_page')
        else:
            error = 'форма была заполенан не верно'
    form = NewPerson()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'authorization/registration_user.html', data)


def favorites(request):
    # Проверяем, авторизован ли пользователь
    user_id = request.session.get('user_id')
    if not user_id:
        # Если пользователь не авторизован, перенаправляем на страницу входа
        messages.error(request, 'Пожалуйста, авторизуйтесь для доступа к избранному.')
        return redirect('login_user')

    # Получаем пользователя и его избранные автомобили
    user = Person.objects.get(id=user_id)
    favorite_cars = user.favorite.all()  # Получаем все избранные автомобили пользователя

    # Передаем список избранных машин в шаблон
    return render(request, 'main/favorites.html', {'favorite_cars': favorite_cars})


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
    car_filter = CarFilter(request.GET, queryset=cars)
    brands = Brand.objects.all()
    drive_types = TransmissionDrive.objects.values_list('drive_type', flat=True).distinct()
    transmissions = TransmissionDrive.objects.values_list('transmission', flat=True).distinct()

    return render(request, 'main/popular.html', {
        'filter': car_filter,
        'brands': brands,
        'drive_types': drive_types,
        'transmissions': transmissions,
        'cars': car_filter.qs
    })


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
    drive_type = request.GET.get('drive_type')
    transmission = request.GET.get('transmission')
    horsepower_min = request.GET.get('horsepower_min')
    horsepower_max = request.GET.get('horsepower_max')

    cars = Car.objects.all()

    if brand_id:
        cars = cars.filter(model__brand_id=brand_id)
    if model_id:
        cars = cars.filter(model_id=model_id)
    if drive_type:
        cars = cars.filter(configuration__transmission_drive__drive_type=drive_type)
    if transmission:
        cars = cars.filter(configuration__transmission_drive__transmission=transmission)
    if horsepower_min:
        cars = cars.filter(configuration__technical_specs__horsepower__gte=horsepower_min)
    if horsepower_max:
        cars = cars.filter(configuration__technical_specs__horsepower__lte=horsepower_max)

    return render(request, 'main/car_list_partial.html', {'cars': cars})



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


def get_models_by_brand(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse({'models': list(models)})
