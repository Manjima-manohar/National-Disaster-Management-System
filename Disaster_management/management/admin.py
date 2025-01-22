from django.contrib import admin
from .models import Person_missing,Camp,Vehicle_management,Public,Fund_request,volunteer_camp_allocation,Police_station,Insurance
# Register your models here.
admin.site.register(Person_missing)
admin.site.register(Camp)
admin.site.register(Vehicle_management)
admin.site.register(Public)
admin.site.register(Fund_request)
admin.site.register(volunteer_camp_allocation)
admin.site.register(Police_station)
admin.site.register(Insurance)