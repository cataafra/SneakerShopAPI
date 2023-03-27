from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Brand)
admin.site.register(Sneaker)
admin.site.register(Garment)
admin.site.register(Customer)
admin.site.register(BoughtGarments)


