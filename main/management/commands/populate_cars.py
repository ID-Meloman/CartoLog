from django.core.management.base import BaseCommand
from main.scripts.car_parser import parse_car_page  # Импорт функции
from main.models import Car12
import random
import time


class Command(BaseCommand):
    help = 'Парсит автомобили с сайта Autospot'

    def handle(self, *args, **kwargs):
        base_url = "https://autospot.ru"
        num_cars = 100
        car_urls = self.generate_random_car_urls(base_url, num_cars)

        # Для каждого автомобиля получаем информацию и сохраняем в БД
        for url in car_urls:
            car_data = parse_car_page(url)
            if car_data:
                if 'title' in car_data:  # Проверяем наличие ключа 'title'
                    self.save_car_to_db(car_data)
                    self.stdout.write(f"Добавлен: {car_data['title']} с ценой {car_data.get('price', 'не указана')}")
                else:
                    self.stdout.write(f"Ошибка: на странице {url} не найдено название автомобиля")

            # Пауза между запросами
            time.sleep(random.uniform(1, 3))

    # Функция для генерации случайных ссылок на автомобили
    def generate_random_car_urls(self, base_url, num_cars=100):
        car_urls = []
        for _ in range(num_cars):
            brand = random.choice(['jaecoo', 'geely', 'kia', 'toyota', 'bmw'])
            model = random.choice(['j8', 'monjaro', 'atlas_pro', 'camry', 'x5'])
            offer_id = random.randint(100000, 400000)
            car_id = random.randint(2000000, 4000000)

            url = f"{base_url}/brands/{brand}/{model}/suv/offer/{offer_id}/?car={car_id}"
            car_urls.append(url)

        return car_urls

    # Сохранение данных в БД
    def save_car_to_db(self, car_data):
        Car12.objects.create(
            title=car_data.get('title', 'Не указано'),  # Используем .get() для безопасного извлечения
            price=car_data.get('price', 'не указана'),
            url=car_data.get('url', ''),
            # добавьте дополнительные поля, если нужно
        )
