from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_sim, name='start_sim'),
    path('step/', views.step, name='step'),
]
