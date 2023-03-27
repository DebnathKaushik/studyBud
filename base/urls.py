from django.urls import path
from . import views


urlpatterns=[
    path('',views.home, name ="name"),
    path('room24/<str:pk>/',views.room, name ="room"),
]