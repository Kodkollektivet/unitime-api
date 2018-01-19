from django.urls import path

from unitime import views

urlpatterns = [
    path('lectures/', views.Lectures.as_view()),
]
