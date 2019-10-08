from django.contrib import admin
from .models import User, History, UserPlate


class UserAdmin(admin.ModelAdmin):
    list_filter = ('name', 'password')
    list_display = ('name', 'password')
    list_per_page = 20
    search_fields = ('name', 'password')


class HistoryAdmin(admin.ModelAdmin):
    list_filter = ('name', 'license_plate')
    list_display = ('name', 'time', 'photograph', 'license_plate', 'type', 'state', 'price')
    list_per_page = 20
    search_fields = ('name', 'license_plate')


class UserPlateAdmin(admin.ModelAdmin):
    list_filter = ('name', 'license_plate')
    list_display = ('name', 'license_plate')
    list_per_page = 20
    search_fields = ('name', 'license_plate')


admin.site.register(User, UserAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(UserPlate, UserPlateAdmin)