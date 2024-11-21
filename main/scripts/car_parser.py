import requests
from bs4 import BeautifulSoup


# Функция для парсинга страницы автомобиля
def parse_car_page(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка доступа к {url}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Проверка на страницу, где автомобиль отсутствует
        error_heading = soup.find('h1', class_='heading_black')
        if error_heading and "Каталог новых авто от официального дилера" in error_heading.text:
            print(f"Автомобиль не найден на странице {url}")
            return None

        car_data = {}

        # Извлечение названия автомобиля
        title_tag = soup.find('h1')
        if title_tag and title_tag.text.strip():
            full_title = title_tag.text.strip()
            # Разделение на бренд и модель
            if ' ' in full_title:
                brand, model = full_title.split(' ', 1)
                car_data['brand'] = brand
                car_data['model'] = model
            else:
                car_data['brand'] = full_title
                car_data['model'] = 'Не указана'

            # техническе характеристики
            engine_type = soup.find('tr', text=lambda t: 'Тип топлива' in t).find_next('td').text.strip()
            engine_capacity = soup.find('tr', text=lambda t: 'Рабочий объём ДВС' in t).find_next('td').text.strip()
            horsepower = soup.find('tr', text=lambda t: 'Максимальная мощность' in t).find_next('td').text.strip()
            torque = soup.find('tr', text=lambda t: 'Максимальный крутящий момент' in t).find_next('td').text.strip()
            emissions_class = soup.find('tr', text=lambda t: 'Норма токсичности выхлопных газов' in t).find_next(
                'td').text.strip()
            # Значения по умолчанию
            fuel_consumption_city = 8.0
            fuel_consumption_highway = 5.0
            # Преобразование типов
            engine_capacity = round(float(engine_capacity) / 1000, 2)  # Перевод из см³ в литры
            horsepower = int(horsepower)
            torque = int(torque)

            car_data['engine_type'] = engine_type
            car_data['engine_capacity'] = engine_capacity
            car_data['horsepower'] = horsepower
            car_data['torque'] = torque
            car_data['fuel_consumption_city'] = fuel_consumption_city
            car_data['fuel_consumption_highway'] = fuel_consumption_highway
            car_data['emissions_class'] = emissions_class


            #трансмиссия
            transmission = soup.find('tr', text=lambda t: 'КПП (управление режимами движения)' in t).find_next(
                'td').text.strip()
            drive_type = soup.find('tr', text=lambda t: 'Привод' in t).find_next('td').text.strip()
            # Значение по умолчанию
            gears_count = 5
            car_data['transmission'] = transmission
            car_data['gears_count'] = gears_count
            car_data['drive_type'] = drive_type

        else:
            print(f"Не найдено название для {url}")
            return None

        return car_data
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return None
