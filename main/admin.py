from django.contrib import admin
from .models import (
    Brand, CarModel, TechnicalSpecs, TransmissionDrive, SuspensionBrakes,
    SafetyFeatures, Comfort, MultimediaConnectivity, AdditionalOptions,
    Configuration, Dealer, Showroom, CarInShowroom, Car, Person, Comparison, Advertising
)

# Register your models here.
models = [
    Brand, CarModel, TechnicalSpecs, TransmissionDrive, SuspensionBrakes,
    SafetyFeatures, Comfort, MultimediaConnectivity, AdditionalOptions,
    Configuration, Dealer, Showroom, CarInShowroom, Car, Person, Comparison, Advertising,
]

for model in models:
    admin.site.register(model)
