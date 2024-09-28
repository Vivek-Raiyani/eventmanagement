from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Facility)
admin.site.register(models.Booking)
admin.site.register(models.BookingSlot)
admin.site.register(models.Maintainance)
admin.site.register(models.Sport)