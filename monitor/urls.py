from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("rooms/create/", views.create_room, name="create_room"),
    path("rooms/<str:room_code>/", views.room_detail, name="room_detail"),
    path(
    "camera/<str:room_code>/",
    views.camera_view,
    name="camera_view",
),
    path(
    "parent/<str:room_code>/",
    views.parent_view,
    name="parent_view",
),
    path('alerts/<str:room_code>/', views.get_alerts, name='get_alerts'),
]