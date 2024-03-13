from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.db import models
from django.urls.resolvers import URLPattern

from .models import Stage, Exam, ExamModule, CustomExam, LoadCSV
from .views import create, load_csv

class ExamModuleInline(admin.TabularInline):
    model = ExamModule
    extra = 1

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['stage', 'month', 'year']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'score', 'career', 'stage']
    list_filter = ['career', 'stage']
    inlines = [ExamModuleInline]

class CustomExamAdmin(admin.ModelAdmin):
    model = CustomExam

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('create/', create, name=view_name),]
    
admin.site.register(CustomExam, CustomExamAdmin)

class LoadCSVAdmin(admin.ModelAdmin):
    model = LoadCSV
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('load/', load_csv, name=view_name),]
    
admin.site.register(LoadCSV, LoadCSVAdmin)