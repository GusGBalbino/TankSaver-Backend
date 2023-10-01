from django.contrib import admin
from django.apps import apps

# Register your models here.

my_models = apps.get_app_config('TankSaverAPI').get_models()

for model in my_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass