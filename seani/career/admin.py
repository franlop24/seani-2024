from django.contrib import admin

from .models import Career

# Register your models here.
@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'level']
    ordering = ['level', 'short_name']