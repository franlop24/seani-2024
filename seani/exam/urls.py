from django.urls import path

from . import views

app_name = 'exam'
urlpatterns = [
    path('', views.home, name='home'),
    path('module/<int:module_id>/question/', views.module, name='module'),
    path('module/<int:module_id>/question/<int:question_id>', views.module, name='module'),
    path('create/', views.create, name='create'),
]