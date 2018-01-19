from django.urls import path

from unitime import views

urlpatterns = [
    path('lectures/', views.LecturesView.as_view()),
    path('course/', views.CourseView.as_view()),
]
