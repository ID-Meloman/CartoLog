from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView, DeleteView, UpdateView, ListView
from main.models import Car, CarModel, Brand, Person, TransmissionDrive, CarInShowroom, Advertising
from .forms import NewModel, NewPerson, LoginForm
from main.filters import CarFilter
from bs4 import BeautifulSoup

def calculator(request):
    return render(request, 'calculate/calculator.html')


class CarCheckView(ListView):
    model = CarInShowroom
    template_name = 'main/car_check.html'
    context_object_name = 'car_in_showroom_list'

    def get_queryset(self):
        # Получаем ID автомобиля из URL параметров
        car_id = self.kwargs['car_id']
        # Возвращаем только те объекты, которые связаны с данным автомобилем
        return CarInShowroom.objects.filter(car__id=car_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем также объект автомобиля для заголовка или другой информации
        context['car'] = Car.objects.get(id=self.kwargs['car_id'])
        return context


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


def toggle_favorite(request, car_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Вы должны быть авторизованы для добавления в избранное.'}, status=403)

    try:
        # Находим пользователя и автомобиль
        user = Person.objects.get(id=user_id)
        car = Car.objects.get(id=car_id)

        # Определяем действие: добавляем или убираем из избранного
        if car in user.favorite.all():
            user.favorite.remove(car)
            is_favorite = False
        else:
            user.favorite.add(car)
            is_favorite = True

        return JsonResponse({'is_favorite': is_favorite})

    except Person.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден.'}, status=404)
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Автомобиль не найден.'}, status=404)


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
    advertising = Advertising.objects.all()
    cars = Car.objects.all()
    car_filter = CarFilter(request.GET, queryset=cars)
    brands = Brand.objects.all()
    drive_types = TransmissionDrive.objects.values_list('drive_type', flat=True).distinct()
    transmissions = TransmissionDrive.objects.values_list('transmission', flat=True).distinct()

    # Получаем текущего пользователя и его избранные автомобили
    user_id = request.session.get('user_id')
    if user_id:
        user = Person.objects.get(id=user_id)
        favorite_cars = user.favorite.all()
        comparison_cars = user.comparison.all()
    else:
        favorite_cars = []
        comparison_cars = []        # Если пользователь не авторизован, избранное пустое

    return render(request, 'main/popular.html', {
        'filter': car_filter,
        'brands': brands,
        'drive_types': drive_types,
        'transmissions': transmissions,
        'cars': car_filter.qs,
        'favorite_cars': favorite_cars,
        'comparison_cars': comparison_cars,
        'ad': advertising,
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

    # Добавляем избранное для текущего пользователя
    user_id = request.session.get('user_id')
    favorite_cars = []
    if user_id:
        user = Person.objects.get(id=user_id)
        favorite_cars = user.favorite.all()
        comparison_cars = user.comparison.all()

    return render(request, 'main/car_list_partial.html', {
        'cars': cars,
        'favorite_cars': favorite_cars,
        'comparison_cars': comparison_cars,
    })


class CarDetail(DetailView):
    model = Car
    template_name = 'main/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение текущего автомобиля
        car = self.get_object()
        context['vk_video_url'] = car.vk_video_url  # Передача ссылки на видео в контекст

        # Получение user_id из сессии
        user_id = self.request.session.get('user_id')
        comparison_cars = []
        favorite_cars = []

        # Если пользователь существует, получить его данные о сравнении и избранном
        if user_id:
            user = Person.objects.get(id=user_id)
            comparison_cars = user.comparison.all()
            favorite_cars = user.favorite.all()

        context['comparison_cars'] = comparison_cars
        context['favorite_cars'] = favorite_cars

        return context


def get_models_by_brand(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse({'models': list(models)})


def comparison_view(request):
    # Проверяем, авторизован ли пользователь
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Пожалуйста, авторизуйтесь для доступа к сравнению автомобилей.')
        return redirect('login_user')

    # Получаем пользователя
    user = get_object_or_404(Person, id=user_id)

    # Получаем все автомобили, добавленные в сравнение
    comparisons = user.comparison.all()  # Получаем все автомобили для сравнения

    # Передаем список автомобилей для сравнения в шаблон
    return render(request, 'main/comparison.html', {'comparisons': comparisons})


def toggle_comparison(request, car_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Вы должны быть авторизованы'}, status=403)

    try:
        car = get_object_or_404(Car, id=car_id)
        user = get_object_or_404(Person, id=user_id)

        # Переключаем состояние сравнения
        is_in_comparison = car in user.comparison.all()
        if is_in_comparison:
            user.comparison.remove(car)
        else:
            user.comparison.add(car)

        return JsonResponse({'is_in_comparison': not is_in_comparison})  # Возвращаем новое состояние
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def remove_comparison(request, car_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'You must be logged in to remove from comparison.'}, status=403)

    try:
        car = get_object_or_404(Car, id=car_id)
        user = get_object_or_404(Person, id=user_id)

        # Remove car from comparison list
        user.comparison.remove(car)

        # Redirecting back to the comparison page
        return redirect(reverse('comparison_view'))  # Replace with your comparison view name if different

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def search_cars(request):
    query = request.GET.get('q', '')
    if query:
        cars = Car.objects.filter(
            Q(model__name__icontains=query) | Q(model__brand__name__icontains=query)
        ).select_related('model__brand')
        results = [
            {
                'id': car.id,
                'brand': car.model.brand.name,
                'model': car.model.name,
                'color': car.color,
            }
            for car in cars
        ]
    else:
        results = []
    return JsonResponse({'results': results})

