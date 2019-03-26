from django.contrib import admin
from webapp.models import UserProfile,room_type,addons,rooms,reservations
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(room_type)
admin.site.register(addons)
admin.site.register(rooms)
admin.site.register(reservations)
# admin.site.register(addon_res)
