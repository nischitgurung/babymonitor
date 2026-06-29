from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

rooms = {}

@csrf_exempt
def offer(request):
    data = json.loads(request.body)
    room = data["room"]

    if room not in rooms:
        rooms[room] = {}

    rooms[room]["offer"] = data["offer"]
    return JsonResponse({"status": "offer stored"})


@csrf_exempt
def answer(request):
    data = json.loads(request.body)
    room = data["room"]

    if room not in rooms:
        rooms[room] = {}

    rooms[room]["answer"] = data["answer"]
    return JsonResponse({"status": "answer stored"})


def get_offer(request, room):
    return JsonResponse({
        "offer": rooms.get(room, {}).get("offer")
    })


def get_answer(request, room):
    return JsonResponse({
        "answer": rooms.get(room, {}).get("answer")
    })