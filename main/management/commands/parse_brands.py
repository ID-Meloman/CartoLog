from django.core.management.base import BaseCommand
from main.models import Brand
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Парсит данные с сайта и сохраняет только марки в базу данных'

    def handle(self, *args, **kwargs):
        url = 'https://www.tts.ru/auto/'  # URL, с которого будем парсить
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }

        # Делаем запрос к странице
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Ищем все элементы, которые содержат марку автомобилей
            # Теперь ищем элементы с классом 'descriprion-model semibold'
            car_elements = soup.find_all('div', class_='descriprion-model semibold')

            # Проверка: если парсер не нашел элементов, выведем это
            if not car_elements:
                self.stdout.write(self.style.ERROR("Марки не найдены на странице!"))
                return

            # Парсим марки и сохраняем в базу
            for car in car_elements:
                make_name = car.text.strip()  # Извлекаем название марки

                # Проверяем, что марка не пустая
                if make_name:
                    brand, created = Brand.objects.get_or_create(name=make_name)

                    # Если марка была создана, выводим сообщение
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Сохранена новая марка: {make_name}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Марка {make_name} уже существует в базе"))
                else:
                    self.stdout.write(self.style.ERROR("Не удалось извлечь название марки для одного из автомобилей."))
        else:
            self.stdout.write(self.style.ERROR(f"Не удалось получить страницу, код ошибки: {response.status_code}"))
