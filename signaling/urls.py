from django.urls import path
from . import views

urlpatterns = [
    path("signal/", views.signaling, kwargs={"role": "generic"}),  # POST for offer/answer/candidate
    path("offer/<str:room>/", views.get_offer),
    path("answer/<str:room>/", views.get_answer),
    path("candidates/<str:room>/<str:side>/", views.get_candidates),
]