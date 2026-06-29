from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

rooms = {}  # room_code -> {"offer": ..., "answer": ..., "candidates": {"camera": [], "parent": []}}

@csrf_exempt
def signaling(request, role):  # Unified endpoint for offer/answer/candidates
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    
    try:
        data = json.loads(request.body)
        room = data.get("room")
        if not room:
            return JsonResponse({"error": "room required"}, status=400)
        
        if room not in rooms:
            rooms[room] = {"offer": None, "answer": None, "candidates": {"camera": [], "parent": []}}
        
        payload = {}
        if "offer" in data:
            rooms[room]["offer"] = data["offer"]
            payload = {"status": "offer stored"}
        elif "answer" in data:
            rooms[room]["answer"] = data["answer"]
            payload = {"status": "answer stored"}
        elif "candidate" in data:
            side = data.get("side", "camera")  # "camera" or "parent"
            rooms[room]["candidates"][side].append(data["candidate"])
            payload = {"status": "candidate stored"}
        else:
            return JsonResponse({"error": "offer/answer/candidate required"}, status=400)
        
        return JsonResponse(payload)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def get_offer(request, room):
    data = rooms.get(room, {})
    return JsonResponse({"offer": data.get("offer")})

def get_answer(request, room):
    data = rooms.get(room, {})
    return JsonResponse({"answer": data.get("answer")})

def get_candidates(request, room, side):
    data = rooms.get(room, {})
    return JsonResponse({"candidates": data.get("candidates", {}).get(side, [])})