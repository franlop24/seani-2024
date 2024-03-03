from django.urls import path

from . import views

app_name = 'exam'
urlpatterns = [
    path('create/', views.create, name='create'),
]