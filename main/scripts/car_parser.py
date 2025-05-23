import requests
from bs4 import BeautifulSoup
import re

from django.template.defaultfilters import title


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
        if title_tag and title_tag.text:
            print(f"проверка: {url}")
            # Разделение на бренд и модель
            parts = title_tag.text.split(' ', 1)  # Разделение строки по первому пробелу
            car_data['brand'] = parts[0]  # Всё до первого пробела — это бренд
            car_data['model'] = parts[1] if len(parts) > 1 else 'Не указана'  # Остальное — это модель, если она есть

            configuration_row = soup.find('td', text=re.compile(r'Комплектация', re.IGNORECASE))
            configuration = configuration_row.find_next('td').text.strip() if configuration_row else 'base'
            car_data['configuration'] = configuration

            # Извлечение технических характеристик
            # Тип топлива
            engine_type_row = soup.find('td', text=re.compile(r'Тип топлива', re.IGNORECASE))
            engine_type = engine_type_row.find_next('td').text.strip() if engine_type_row else '0'

            engine_capacity_row = soup.find('td', text=re.compile(r'Рабочий объём ДВС', re.IGNORECASE))
            engine_capacity = engine_capacity_row.find_next('td').text.strip() if engine_capacity_row else '0'

            horsepower_row = soup.find('td', text=re.compile(r'Максимальная мощность', re.IGNORECASE))
            horsepower = horsepower_row.find_next('td').text.strip() if horsepower_row else '0'

            torque_row = soup.find('td', text=re.compile(r'Максимальный крутящий момент', re.IGNORECASE))
            torque = torque_row.find_next('td').text.strip() if torque_row else '0'

            emissions_class_row = soup.find('td', text=re.compile(r'Норма токсичности выхлопных газов', re.IGNORECASE))
            emissions_class = emissions_class_row.find_next('td').text.strip() if emissions_class_row else '0'

            # Преобразование значений в соответствующие типы данных
            try:
                engine_capacity = round(float(engine_capacity) / 1000, 2) if engine_capacity != '0' else 0
                horsepower = int(horsepower) if horsepower != '0' else 0
                torque = int(torque) if torque != '0' else 0
            except ValueError:
                engine_capacity = horsepower = torque = 0  # Обработка ошибок преобразования

            # Присваивание значений в словарь car_data
            car_data.update({
                'engine_type': engine_type,
                'engine_capacity': engine_capacity,
                'horsepower': horsepower,
                'torque': torque,
                'fuel_consumption_city': 8.0,  # Значение по умолчанию
                'fuel_consumption_highway': 5.0,  # Значение по умолчанию
                'emissions_class': emissions_class
            })

            # Трансмиссия
            transmission_row = soup.find('td', text=lambda t: 'КПП (управление режимами движения)' in t)
            if transmission_row:
                transmission = transmission_row.find_next('td').text.strip()
            else:
                transmission = 'Не указана'  # Значение по умолчанию, если строка не найдена
            # Привод
            drive_type_row = soup.find('td', text=lambda t: 'Привод' in t)
            if drive_type_row:
                drive_type = drive_type_row.find_next('td').text.strip()
            else:
                drive_type = 'Не указан'  # Значение по умолчанию, если строка не найдена
            # Количество передач (по умолчанию)
            gears_count = 5  # Установить значение по умолчанию для количества передач
            # Запись данных в словарь
            car_data['transmission'] = transmission
            car_data['gears_count'] = gears_count
            car_data['drive_type'] = drive_type

            # Таблица безопасности
            # Проверка и извлечение количества подушек безопасности
            airbags_count_row = soup.find('td', text=lambda t: 'Подушки безопасности, шт' in t)
            airbags_count = int(airbags_count_row.find_next('td').text.strip()) if airbags_count_row else 0
            # Проверка и извлечение информации о наличии антиблокировочной системы (ABS)
            abs_row = soup.find('td', text=lambda t: 'Антиблокировочная система' in t)
            abs_feature = abs_row.find_next('td').text.strip() if abs_row else False
            abs_feature = True if abs_feature == 'есть' else False
            # Проверка и извлечение информации о наличии электронной системы динамической стабилизации (ESP)
            esp_row = soup.find('td', text=lambda t: 'Электронная система динамической стабилизации' in t)
            esp = esp_row.find_next('td').text.strip() if esp_row else False
            esp = True if esp == 'есть' else False
            # Проверка и извлечение информации о наличии контроля тяги/пробуксовки
            traction_control_row = soup.find('td', text=lambda t: 'Контроль тяги/пробуксовки' in t)
            traction_control = traction_control_row.find_next('td').text.strip() if traction_control_row else False
            traction_control = True if traction_control == 'есть' else False
            # Проверка и извлечение информации о наличии системы удержания полосы движения
            lane_assist_row = soup.find('td', text=lambda t: 'Удержание полосы движения' in t)
            lane_assist = lane_assist_row.find_next('td').text.strip() if lane_assist_row else False
            lane_assist = True if lane_assist == 'есть' else False
            # Проверка и извлечение информации о наличии системы мониторинга мертвых зон
            blind_spot_monitoring_row = soup.find('td', text=lambda t: 'Контроль мертвых зон/боковых интервалов' in t)
            blind_spot_monitoring = blind_spot_monitoring_row.find_next(
                'td').text.strip() if blind_spot_monitoring_row else False
            blind_spot_monitoring = True if blind_spot_monitoring == 'есть' else False
            # Проверка и извлечение информации о наличии адаптивного круиз-контроля
            adaptive_cruise_control_row = soup.find('td', text=lambda t: 'Круиз-контроль' in t)
            adaptive_cruise_control = adaptive_cruise_control_row.find_next(
                'td').text.strip() if adaptive_cruise_control_row else False
            adaptive_cruise_control = True if adaptive_cruise_control == 'есть' else False

            # Добавление в словарь данных автомобиля
            car_data['airbags_count'] = airbags_count
            car_data['abs'] = abs_feature
            car_data['esp'] = esp
            car_data['traction_control'] = traction_control
            car_data['lane_assist'] = lane_assist
            car_data['blind_spot_monitoring'] = blind_spot_monitoring
            car_data['adaptive_cruise_control'] = adaptive_cruise_control

            # Таблица комфорта
            # Проверка и извлечение информации о кондиционировании и климат-контроле
            climate_control_row = soup.find('td', text=lambda t: 'Кондиционирование и климат-контроль' in t)
            climate_control = climate_control_row.find_next('td').text.strip() if climate_control_row else False
            climate_control = True if climate_control == 'климат-контроль' else False
            # Проверка и извлечение информации о наличии отдельной системы кондиционирования для пассажиров
            climate_zones_row = soup.find('td',
                                          text=lambda t: 'Отдельная система кондиционирования для пассажиров' in t)
            climate_zones = climate_zones_row.find_next('td').text.strip() if climate_zones_row else 0
            climate_zones = 2 if climate_zones == 'есть' else 1
            # Проверка и извлечение информации о материале обивки сидений
            seat_material_row = soup.find('td', text=lambda t: 'Обивка сидений' in t)
            seat_material = seat_material_row.find_next('td').text.strip() if seat_material_row else 'не указано'
            # Проверка и извлечение информации о наличии обогрева сидений
            front_seat_heating_row = soup.find('td', text=lambda t: 'Обогрев сидений' in t)
            front_seat_heating = front_seat_heating_row.find_next(
                'td').text.strip() if front_seat_heating_row else False
            front_seat_heating = True if front_seat_heating == 'есть' else False
            # Проверка и извлечение информации о наличии вентиляции сидений
            seat_ventilation_row = soup.find('td', text=lambda t: 'Вентиляция сидений' in t)
            seat_ventilation = seat_ventilation_row.find_next('td').text.strip() if seat_ventilation_row else False
            seat_ventilation = True if seat_ventilation == 'есть' else False
            # Проверка и извлечение информации о наличии панорамной крыши
            panoramic_roof_row = soup.find('td', text=lambda t: 'Панорамная крыша' in t)
            panoramic_roof = panoramic_roof_row.find_next('td').text.strip() if panoramic_roof_row else False
            panoramic_roof = True if panoramic_roof == 'есть' else False
            # Проверка и извлечение информации о наличии люка
            sunroof_row = soup.find('td', text=lambda t: 'Люк' in t)
            sunroof = sunroof_row.find_next('td').text.strip() if sunroof_row else False
            sunroof = True if sunroof == 'есть' else False
            # Проверка и извлечение информации о наличии электропривода сидений
            electric_adjustments_seat_row = soup.find('td', text=lambda t: 'Электропривод сидений' in t)
            electric_adjustments_seat = electric_adjustments_seat_row.find_next(
                'td').text.strip() if electric_adjustments_seat_row else False
            electric_adjustments_seat = True if electric_adjustments_seat == 'есть' else False
            # Проверка и извлечение информации о наличии памяти настроек сидений
            seat_adjustment_positions_row = soup.find('td', text=lambda t: 'Память настроек' in t)
            seat_adjustment_positions = seat_adjustment_positions_row.find_next(
                'td').text.strip() if seat_adjustment_positions_row else 0
            seat_adjustment_positions = 3 if seat_adjustment_positions == 'есть' else 0

            # Значение по умолчанию для обогрева задних сидений
            rear_seat_heating = False

            # Добавление в словарь данных автомобиля
            car_data['climate_control'] = climate_control
            car_data['climate_zones'] = climate_zones
            car_data['seat_material'] = seat_material
            car_data['front_seat_heating'] = front_seat_heating
            car_data['rear_seat_heating'] = rear_seat_heating
            car_data['seat_ventilation'] = seat_ventilation
            car_data['panoramic_roof'] = panoramic_roof
            car_data['sunroof'] = sunroof
            car_data['electric_adjustments_seat'] = electric_adjustments_seat
            car_data['seat_adjustment_positions'] = seat_adjustment_positions

            # Таблица дополнительных опций
            # Значение по умолчанию для прицепного устройства
            tow_bar = False
            # Проверка и извлечение информации о наличии усиленной/адаптивной подвески
            adaptive_suspension_row = soup.find('td', text=lambda t: 'Усиленная/адаптивная/регулируемая подвеска' in t)
            adaptive_suspension = adaptive_suspension_row.find_next(
                'td').text.strip() if adaptive_suspension_row else False
            adaptive_suspension = True if adaptive_suspension == 'есть' else False
            #            # Проверка и извлечение информации о наличии дистанционного/бесконтактного открывания багажника/задней двери
            remote_start_row = soup.find('td', text=lambda
                t: 'Дистанционное/бесконтактное открывание багажника/задней двери' in t)
            remote_start = remote_start_row.find_next('td').text.strip() if remote_start_row else False
            remote_start = True if remote_start == 'есть' else False
            # Проверка и извлечение информации о наличии системы автоматической парковки
            parking_assistance_row = soup.find('td', text=lambda t: 'Система автоматической парковки' in t)
            parking_assistance = parking_assistance_row.find_next(
                'td').text.strip() if parking_assistance_row else False
            parking_assistance = True if parking_assistance == 'есть' else False
            # Проверка и извлечение информации о наличии камеры 360°
            camera_360_row = soup.find('td', text=lambda t: 'Видеокамера' in t)
            camera_360 = camera_360_row.find_next('td').text.strip() if camera_360_row else False
            camera_360 = True if camera_360 == 'есть' else False

            # Сохранение данных в словарь
            car_data['tow_bar'] = tow_bar
            car_data['adaptive_suspension'] = adaptive_suspension
            car_data['remote_start'] = remote_start
            car_data['parking_assistance'] = parking_assistance
            car_data['camera_360'] = camera_360

            # Таблица автомобиля
            # Цвет кузова
            color_row = soup.find('div', class_='card-auto_used-characteristics_item',
                                  attrs={'data-before': 'Цвет кузова'})
            color = color_row.find('div').text.strip() if color_row else 'Не указан'

            # Размер дисков
            wheel_size_row = soup.find('td', text=lambda t: t and 'Размер дисков' in t)
            if wheel_size_row:
                wheel_size = wheel_size_row.find_next('td').text.strip()
                # Проверяем, начинается ли с 'R' и последующие символы являются числом
                if wheel_size.startswith('R') and wheel_size[1:].isdigit():
                    wheel_size = int(wheel_size[1:])  # Извлекаем число после 'R'
                elif wheel_size.isdigit():  # Если нет 'R', просто проверяем, является ли это числом
                    wheel_size = int(wheel_size)
                else:
                    wheel_size = 0  # Если формат неизвестен, устанавливаем 0
            else:
                wheel_size = 0  # Если строка не найдена

            # Светодиодные фары
            led_headlights_row = soup.find('td', text=lambda t: t and 'Фары' in t)
            if led_headlights_row:
                led_headlights = led_headlights_row.find_next('td').text.strip().lower()
                led_headlights = 'светодиодные' in led_headlights
            else:
                led_headlights = False

            # Противотуманные фары
            fog_lights_row = soup.find('td', text=lambda t: t and 'Противотуманные фары' in t)
            if fog_lights_row:
                fog_lights = fog_lights_row.find_next('td').text.strip()
                fog_lights = fog_lights == 'есть'
            else:
                fog_lights = False

            # Тонированные стекла
            tinted_windows_row = soup.find('td', text=lambda t: t and 'Тонированное остекление' in t)
            if tinted_windows_row:
                tinted_windows = tinted_windows_row.find_next('td').text.strip()
                tinted_windows = tinted_windows == 'есть'
            else:
                tinted_windows = False

            # Рейлинги на крыше
            roof_rails_row = soup.find('td', text=lambda t: t and 'Система перевозки багажа на крыше' in t)
            if roof_rails_row:
                roof_rails = roof_rails_row.find_next('td').text.strip()
                roof_rails = roof_rails == 'есть'
            else:
                roof_rails = False

            # Сохранение данных в словарь
            car_data['color'] = color
            car_data['wheel_size'] = wheel_size
            car_data['led_headlights'] = led_headlights
            car_data['fog_lights'] = fog_lights
            car_data['tinted_windows'] = tinted_windows
            car_data['roof_rails'] = roof_rails

            # Ищем элементы <a> с классом, содержащим "lightgallery__item"
            image_elements = soup.select('a.lightgallery__item')
            # Извлекаем ссылки на изображения
            image_urls = [element['href'] for element in image_elements if 'href' in element.attrs]
            # Оставляем только первые пять изображений
            image_urls = image_urls[:5]
            # Сохраняем ссылки на изображения в car_data['images']
            car_data['images'] = image_urls

            return car_data

        else:
            print(f"Не найдено название для {url}")
            return None

    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return None
