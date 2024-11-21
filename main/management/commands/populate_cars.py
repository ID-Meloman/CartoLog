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
            if car_data and 'brand' in car_data:
                brand_name = car_data['brand']
                brand = Brand.objects.filter(name__iexact=brand_name).first()

            if brand:
                model_name = car_data['model']
                car_model = self.save_model(brand, model_name)

                # После сохранения модели автомобиля создаём конфигурацию
                if car_model:
                    self.save_full_configuration(car_model, car_data)

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
        technical_specs = TechnicalSpecs.objects.create(**specs_data)

        transmission_data = {
            'transmission': car_data['transmission'],
            'gears_count': car_data['gears_count'],
            'drive_type': car_data['drive_type'],
        }
        transmission_drive = TransmissionDrive.objects.create(**transmission_data)

        suspension_data = {
            'front_suspension': "Независимая",
            'rear_suspension': "Полузависимая",
            'front_brakes': "Дисковые",
            'rear_brakes': "Барабанные",
        }
        suspension_brakes = SuspensionBrakes.objects.create(**suspension_data)

        safety_data = {
            'airbags_count': 6,
            'abs': True,
            'esp': True,
            'traction_control': True,
            'lane_assist': True,
            'blind_spot_monitoring': True,
            'adaptive_cruise_control': True,
        }
        safety_features = SafetyFeatures.objects.create(**safety_data)

        comfort_data = {
            'name': f"{car_model.name} Comfort",
            'climate_control': True,
            'climate_zones': 2,
            'seat_material': "Кожа",
            'front_seat_heating': True,
            'rear_seat_heating': True,
            'seat_ventilation': True,
            'panoramic_roof': False,
            'sunroof': True,
            'electric_adjustments_seat': True,
            'seat_adjustment_positions': 8,
        }
        comfort = Comfort.objects.create(**comfort_data)

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
        multimedia_connectivity = MultimediaConnectivity.objects.create(**multimedia_data)

        options_data = {
            'tow_bar': False,
            'adaptive_suspension': False,
            'remote_start': True,
            'parking_assistance': True,
            'camera_360': True,
        }
        additional_options = AdditionalOptions.objects.create(**options_data)

        # Создаём конфигурацию
        configuration = Configuration.objects.create(
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
        car = Car.objects.create(
            model=car_model,
            configuration=configuration,
            color="Белый",
            wheel_size=17.0,
            led_headlights=True,
            fog_lights=True,
            tinted_windows=False,
            roof_rails=True,
        )

        self.stdout.write(f"Автомобиль {car_model.name} успешно добавлен с конфигурацией {configuration.name}")
