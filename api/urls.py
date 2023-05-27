from django.urls import path
from . import views

urlpatterns = [
    path('validate/<str:number>/', views.validate),
    path('auth/register/', views.register),
    path('auth/login/', views.login),
    path('reports/', views.ReportView.as_view()),
]
