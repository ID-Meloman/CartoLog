from django.core.management.base import BaseCommand
from main.scripts.car_parser import parse_car_page
from main.models import (
    Brand, CarModel, TechnicalSpecs, TransmissionDrive, SuspensionBrakes,
    SafetyFeatures, Comfort, MultimediaConnectivity, AdditionalOptions, Configuration, Car
)
import time
import random


class Command(BaseCommand):
    help = 'Парсит автомобили и записывает в базу данных'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаю парсинг автомобилей с TTS.ru...")

        # Генерируем случайные 100 ID для парсинга
        num_pages = 100
        id_range = (1790000, 1810000)  # Пример диапазона ID
        random_ids = random.sample(range(*id_range), num_pages)

        for auto_id in random_ids:
            url = f"https://www.tts.ru/auto/detail.php?auto={auto_id}"

            # Парсим данные с текущей страницы
            car_data = parse_car_page(url)
            print(car_data)

            # Проверяем, что данные есть и что brand существует
            if car_data:
                brand_name = car_data['brand']

                # Если brand_name пустой, логируем ошибку или пропускаем эту итерацию
                if not brand_name:
                    self.stdout.write(f"Ошибка: бренд не указан для автомобиля с URL: {url}")
                    continue  # Пропускаем текущую итерацию, если бренд не найден

                # Ищем бренд в базе данных
                brand = Brand.objects.filter(name__iexact=brand_name).first()

                # Если бренд найден, продолжаем работу с моделью
                if brand:
                    model_name = car_data.get('model',
                                              'Неизвестная модель')  # Если модель не указана, используем значение по умолчанию
                    car_model = self.save_model(brand, model_name)
                    if car_model:
                        self.save_full_configuration(car_model, car_data)
                else:
                    self.stdout.write(f"Бренд '{brand_name}' не найден в базе данных. Пропускаем автомобиль.")

    def save_model(self, brand, model_name):
        car_model, created = CarModel.objects.get_or_create(
            name=model_name,
            brand=brand
        )
        if created:
            self.stdout.write(f"Добавлена модель: {model_name} (Бренд: {brand.name})")
        else:
            self.stdout.write(f"Модель уже существует: {model_name} (Бренд: {brand.name})")
        return car_model

    def save_full_configuration(self, car_model, car_data):
        specs_data = {
            'name': f"{car_model.name} Specs",
            'engine_type': car_data['engine_type'],
            'engine_capacity': car_data['engine_capacity'],
            'horsepower': car_data['horsepower'],
            'torque': car_data['torque'],
            'fuel_consumption_city': car_data['fuel_consumption_city'],
            'fuel_consumption_highway': car_data['fuel_consumption_highway'],
            'emissions_class': car_data['emissions_class'],
        }
        technical_specs, created = TechnicalSpecs.objects.get_or_create(**specs_data)

        transmission_data = {
            'transmission': car_data['transmission'],
            'gears_count': car_data['gears_count'],
            'drive_type': car_data['drive_type'],
        }
        transmission_drive, created = TransmissionDrive.objects.get_or_create(**transmission_data)

        suspension_data = {
            'front_suspension': "Независимая",
            'rear_suspension': "Полузависимая",
            'front_brakes': "Дисковые",
            'rear_brakes': "Дисковые",
        }
        suspension_brakes, created = SuspensionBrakes.objects.get_or_create(**suspension_data)

        safety_data = {
            'airbags_count': car_data['airbags_count'],
            'abs': car_data['abs'],
            'esp': car_data['esp'],
            'traction_control': car_data['traction_control'],
            'lane_assist': car_data['lane_assist'],
            'blind_spot_monitoring': car_data['blind_spot_monitoring'],
            'adaptive_cruise_control': car_data['adaptive_cruise_control'],
        }
        safety_features, created = SafetyFeatures.objects.get_or_create(**safety_data)

        comfort_data = {
            'name': f"{car_model.name} Comfort",
            'climate_control': car_data['climate_control'],
            'climate_zones': car_data['climate_zones'],
            'seat_material': car_data['seat_material'],
            'front_seat_heating': car_data['front_seat_heating'],
            'rear_seat_heating': car_data['rear_seat_heating'],
            'seat_ventilation': car_data['seat_ventilation'],
            'panoramic_roof': car_data['panoramic_roof'],
            'sunroof': car_data['sunroof'],
            'electric_adjustments_seat': car_data['electric_adjustments_seat'],
            'seat_adjustment_positions': car_data['seat_adjustment_positions'],
        }
        comfort, created = Comfort.objects.get_or_create(**comfort_data)

        multimedia_data = {
            'name': f"{car_model.name} Multimedia",
            'infotainment_system': True,
            'screen_size': 10.1,
            'navigation_system': True,
            'speakers_count': 6,
            'wireless_communication': True,
            'usb_ports': 3,
            'apple_carplay': True,
            'android_auto': True,
        }
        multimedia_connectivity, created = MultimediaConnectivity.objects.get_or_create(**multimedia_data)

        options_data = {
            'tow_bar': car_data['tow_bar'],
            'adaptive_suspension': car_data['adaptive_suspension'],
            'remote_start': car_data['remote_start'],
            'parking_assistance': car_data['parking_assistance'],
            'camera_360': car_data['camera_360'],
        }
        additional_options, created = AdditionalOptions.objects.get_or_create(**options_data)

        # Создаём конфигурацию
        configuration, created = Configuration.objects.get_or_create(
            name=f"{car_model.name} Configuration",
            technical_specs=technical_specs,
            transmission_drive=transmission_drive,
            suspension_brakes=suspension_brakes,
            safety_features=safety_features,
            comfort=comfort,
            multimedia_connectivity=multimedia_connectivity,
            additional_options=additional_options,
        )

        # Создаём запись автомобиля
        car, created = Car.objects.get_or_create(
            model=car_model,
            configuration=configuration,
            color= car_data['color'],
            wheel_size= car_data['wheel_size'],
            led_headlights= car_data['led_headlights'],
            fog_lights= car_data['fog_lights'],
            tinted_windows=car_data['tinted_windows'],
            roof_rails=car_data['roof_rails'],
        )
        if created == True:
            print(f"{car.model} {car.color} добавленна")

        self.stdout.write(f"Автомобиль {car_model.name} успешно добавлен с конфигурацией {configuration.name}")
