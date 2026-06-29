from django.urls import path
from . import views

urlpatterns = [
    path("offer/", views.offer),
    path("answer/", views.answer),
    path("offer/<str:room>/", views.get_offer),
    path("answer/<str:room>/", views.get_answer),
]