from django.contrib import admin
from .models import Test


class TestAdmin(admin.ModelAdmin):
    list_filter = ('id', 'num')
    list_display = ('id', 'num')
    list_per_page = 20
    search_fields = ('id', 'num')


admin.site.register(Test, TestAdmin)