from django.contrib import admin

from .models import Stage, Exam, ExamModule

class ExamModuleInline(admin.TabularInline):
    model = ExamModule
    extra = 1

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['stage', 'month', 'year']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'career', 'stage']
    list_filter = ['career', 'stage']
    inlines = [ExamModuleInline]