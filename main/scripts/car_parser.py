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

        car_data = {}
        car_data['url'] = url

        # Извлечение названия автомобиля
        title_tag = soup.find('h1', class_='offer-container__car-title')
        if title_tag:
            car_data['title'] = title_tag.text.strip()
        else:
            print(f"Не найдено название для {url}")  # Логирование ошибки

        # Извлечение цены
        price_tag = soup.find('div', class_='offer-main-characteristic__value')
        if price_tag:
            car_data['price'] = price_tag.text.strip()

        return car_data
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return None
