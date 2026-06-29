from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room
from django.http import JsonResponse
from .models import Alert
from .motion_detector import MotionDetector
# Global registry
motion_detectors = {}
def home(request):

    return render(request, "home.html")

@login_required
def dashboard(request):

    context = {

        "camera_count": 1,

        "alert_count": 0,

    }

    return render(
        request,
        "dashboard/index.html",
        context
    )
@login_required
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")

        room = Room.objects.create(
            room_name=room_name,
            created_by=request.user
        )

        return redirect("room_detail", room.room_code)

    return render(request, "rooms/create_room.html")


@login_required
def room_detail(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)

    return render(
        request,
        "rooms/room_detail.html",
        {"room": room}
    )
@login_required
def camera_view(request, room_code):

    room = get_object_or_404(
        Room,
        room_code=room_code
    )

    return render(
        request,
        "camera/index.html",
        {
            "room": room
        }
    )
@login_required
def parent_view(request, room_code):

    room = get_object_or_404(
        Room,
        room_code=room_code
    )

    return render(
        request,
        "parent/index.html",
        {
            "room": room
        }
    )
@login_required
def camera_view(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)
    
    # Temporarily disable auto motion detection to avoid conflict
    # if room_code in motion_detectors:
    #     motion_detectors[room_code].stop()
    
    return render(request, "camera/index.html", {"room": room})
@login_required
def get_alerts(request, room_code):
    """API to fetch latest alerts for parent dashboard"""
    room = get_object_or_404(Room, room_code=room_code)
    alerts = Alert.objects.filter(room=room).order_by('-timestamp')[:10]
    
    data = [{
        'id': alert.id,
        'timestamp': alert.timestamp.strftime('%H:%M:%S'),
        'message': alert.message or 'Motion detected',
        'image': alert.image.url if alert.image else None
    } for alert in alerts]
    
    return JsonResponse({'alerts': data})