from django.db import models
from django.conf import settings


class Advertising(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Бренд')
    image = models.ImageField(upload_to='ad_images/', verbose_name='Реклама', blank=True, null=True)
    url = models.URLField(verbose_name='Ссылка на рекламный сайт', blank=True, null=True)

    def __str__(self):
        return self.brand




# Таблица марок
class Brand(models.Model):
    name = models.CharField(max_length=20, verbose_name='Марка автомобиля')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


# Таблица моделей
class CarModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Модель автомобиля')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Марка автомобиля')

    def __str__(self):
        return f'{self.brand} - {self.name}'

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


# Таблица технических характеристик
class TechnicalSpecs(models.Model):
    name = models.CharField(max_length=20, verbose_name='Наименование характеристик')
    engine_type = models.CharField(max_length=20, verbose_name='Тип двигателя')
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Объем двигателя')
    horsepower = models.IntegerField(verbose_name='Лошадиные силы')
    torque = models.IntegerField(verbose_name='Крутящий момент')
    fuel_consumption_city = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Расход по городу')
    fuel_consumption_highway = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Расход по трассе')
    emissions_class = models.CharField(max_length=50, verbose_name='Экологический класс')

    def __str__(self):
        return f'{self.name} - {self.engine_type} - {self.engine_capacity}'

    class Meta:
        verbose_name = 'Двигатель'


# Таблица трансмиссии и привода
class TransmissionDrive(models.Model):
    transmission = models.CharField(max_length=20, verbose_name='Коробка передач')
    gears_count = models.IntegerField(verbose_name='Количество передач')
    drive_type = models.CharField(max_length=20, verbose_name='Привод')

    def __str__(self):
        return f'{self.transmission} - {self.gears_count}, {self.drive_type}'

    class Meta:
        verbose_name = 'Трансмиссия и привод'


# Таблица подвески и тормозов
class SuspensionBrakes(models.Model):
    front_suspension = models.CharField(max_length=255, verbose_name='Тип передней подвески')
    rear_suspension = models.CharField(max_length=255, verbose_name='Тип задней подвески')
    front_brakes = models.CharField(max_length=255, verbose_name='Тип передних тормозов')
    rear_brakes = models.CharField(max_length=255, verbose_name='Тип задних тормозов')

    def __str__(self):
        return f'{self.front_suspension}, {self.rear_suspension}, {self.front_brakes}, {self.rear_brakes}'

    class Meta:
        verbose_name = 'Подвеска и тормоза'


# Таблица безопасности
class SafetyFeatures(models.Model):
    airbags_count = models.IntegerField(verbose_name='Количество подушек')
    abs = models.BooleanField(verbose_name='Антиблокировочная система (ABS)')
    esp = models.BooleanField(verbose_name='Система курсовой устойчивости (ESP)')
    traction_control = models.BooleanField(verbose_name='Контроль тяги')
    lane_assist = models.BooleanField(verbose_name='Помощь в удержании полосы движения')
    blind_spot_monitoring = models.BooleanField(verbose_name='Мониторинг слепых зон')
    adaptive_cruise_control = models.BooleanField(verbose_name='Адаптивный круиз-контроль')

    def __str__(self):
        return f'{self.airbags_count} Airbags, ABS: {self.abs}'

    class Meta:
        verbose_name = 'Безопасность'


# Таблица комфорта
class Comfort(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название уровня комфорта')
    climate_control = models.BooleanField(verbose_name='Климат-контроль')
    climate_zones = models.IntegerField(verbose_name='Количество зон климат-контроля')
    seat_material = models.CharField(max_length=50, verbose_name='Материал сидений')
    front_seat_heating = models.BooleanField(verbose_name='Подогрев передних сидений')
    rear_seat_heating = models.BooleanField(verbose_name='Подогрев задних сидений')
    seat_ventilation = models.BooleanField(verbose_name='Вентиляция сидений')
    panoramic_roof = models.BooleanField(verbose_name='Панорамная крыша')
    sunroof = models.BooleanField(verbose_name='Люк')
    electric_adjustments_seat = models.BooleanField(verbose_name='Электрическая регулировка сидений')
    seat_adjustment_positions = models.IntegerField(verbose_name='Количество положений регулировки сидений')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комфорт'


# Таблица мультимедиа
class MultimediaConnectivity(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название мультимедиа')
    infotainment_system = models.BooleanField(verbose_name='Мультимедиа')
    screen_size = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Размер экрана')
    navigation_system = models.BooleanField(verbose_name='Навигатор')
    speakers_count = models.IntegerField(verbose_name='Количество динамиков')
    wireless_communication = models.BooleanField(verbose_name='Беспроводная связь')
    usb_ports = models.IntegerField(verbose_name='USB порты')
    apple_carplay = models.BooleanField(verbose_name='Поддержка Apple CarPlay')
    android_auto = models.BooleanField(verbose_name='Поддержка Android Auto')

    def __str__(self):
        return f'{self.name}, {self.screen_size}'

    class Meta:
        verbose_name = 'Мультимедиа'


# Таблица дополнительных опций
class AdditionalOptions(models.Model):
    tow_bar = models.BooleanField(verbose_name='Фаркоп')
    adaptive_suspension = models.BooleanField(verbose_name='Пневмоподвеска')
    remote_start = models.BooleanField(verbose_name='Дистанционный запуск')
    parking_assistance = models.BooleanField(verbose_name='Помощь при парковке')
    camera_360 = models.BooleanField(verbose_name='Камера 360')

    def __str__(self):
        return f'Фаркоп:{self.tow_bar}, Пневмо:{self.adaptive_suspension}, Дист пуск:{self.remote_start}, Парк мод:{self.parking_assistance}'

    class Meta:
        verbose_name = 'Дополнительные опции'


# Основная таблица комплектаций
class Configuration(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название конфигурации')
    technical_specs = models.ForeignKey(TechnicalSpecs, on_delete=models.CASCADE, verbose_name='Технические характеристики')
    transmission_drive = models.ForeignKey(TransmissionDrive, on_delete=models.CASCADE, verbose_name='Трансмиссия')
    suspension_brakes = models.ForeignKey(SuspensionBrakes, on_delete=models.CASCADE, verbose_name='Подвеска и тормоза')
    safety_features = models.ForeignKey(SafetyFeatures, on_delete=models.CASCADE, verbose_name='Безопасность')
    comfort = models.ForeignKey(Comfort, on_delete=models.CASCADE, verbose_name='Комфорт')
    multimedia_connectivity = models.ForeignKey(MultimediaConnectivity, on_delete=models.CASCADE, verbose_name='Мультимедиа')
    additional_options = models.ForeignKey(AdditionalOptions, on_delete=models.CASCADE, verbose_name='Дополнительные опции')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'


# Таблица машин
class Car(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Модель автомобиля')
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, verbose_name='Конфигурация')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    wheel_size = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Размер колес')
    led_headlights = models.BooleanField(verbose_name='LED фары')
    fog_lights = models.BooleanField(verbose_name='Противотуманные фары')
    tinted_windows = models.BooleanField(verbose_name='Тонированные стекла')
    roof_rails = models.BooleanField(verbose_name='Рейлинги на крыше')
    image = models.ImageField(upload_to='car_images/', verbose_name='Изображение общее', blank=True, null=True)
    image_front = models.ImageField(upload_to='car_images/', verbose_name='Изображение спереди', blank=True, null=True)
    image_side = models.ImageField(upload_to='car_images/', verbose_name='Изображение сбоку', blank=True, null=True)
    image_back = models.ImageField(upload_to='car_images/', verbose_name='Изображение сзади', blank=True, null=True)
    image_interior = models.ImageField(upload_to='car_images/', verbose_name='Изображение внутри', blank=True, null=True)
    vk_video_url = models.URLField(verbose_name='Ссылка на видео ВКонтакте', blank=True, null=True)

    def __str__(self):
        return f'{self.model} - {self.configuration} - {self.color}'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Dealer(models.Model):
    name = models.CharField(max_length=30, verbose_name='Наименование организации')
    legal_address = models.CharField(max_length=50, verbose_name='Юридический адрес')
    contact = models.CharField(max_length=15, verbose_name='Контакт автодиллера')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дилер'
        verbose_name_plural = 'Дилеры'


class Showroom(models.Model):
    name = models.CharField(max_length=30, verbose_name='Наименование автосалона')
    address = models.CharField(max_length=50, verbose_name='Адрес')
    contact = models.CharField(max_length=15, verbose_name='Контакт автосалона')
    website = models.CharField(max_length=50, verbose_name='Сайт автосалона')
    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, verbose_name='Дилер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автосалон'
        verbose_name_plural = 'Автосалоны'


class CarInShowroom(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE, verbose_name='Автосалон')
    quantity = models.IntegerField(verbose_name='Количество в наличии')
    price = models.IntegerField(verbose_name='Цена')
    url = models.URLField(verbose_name='Ссылка на автомобиль в автосалоне', blank=True, null=True)

    def __str__(self):
        return f'{self.car} - {self.showroom} - {self.quantity}'

    class Meta:
        verbose_name = 'Машины в наличии'
        verbose_name_plural = 'Машины в наличии'


class Person(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя пользователя')
    email = models.CharField(max_length=50, verbose_name='Почта пользователя')
    password = models.CharField(max_length=50, verbose_name='Пароль пользователя')
    favorite = models.ManyToManyField(Car, related_name='favorited_by', blank=True, verbose_name='Избранные автомобили')
    comparison = models.ManyToManyField(Car, related_name='compared_by', blank=True, verbose_name='Сравниваемые автомобили')

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



class Comparison(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')
        verbose_name = 'Сравнение'
        verbose_name_plural = 'Сравнения'