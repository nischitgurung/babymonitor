import cv2
import numpy as np
import time
import threading
from django.conf import settings
import os

class MotionDetector:
    def __init__(self, room_code, min_area=500, cooldown=5):
        self.room_code = room_code
        self.min_area = min_area          # Minimum contour area to trigger alert
        self.cooldown = cooldown          # Seconds between alerts
        self.last_alert = 0
        self.running = False
        self.cap = None
        self.thread = None
        
        # Background subtractor
        self.back_sub = cv2.createBackgroundSubtractorMOG2(
            history=500, 
            varThreshold=50, 
            detectShadows=True
        )

    def start(self, camera_index=0):
        """Start motion detection in background thread"""
        if self.running:
            return
        
        self.cap = cv2.VideoCapture(camera_index)
        self.running = True
        self.thread = threading.Thread(target=self._detect_loop, daemon=True)
        self.thread.start()
        print(f"Motion detection started for room {self.room_code}")

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def _detect_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            # Apply background subtraction
            fg_mask = self.back_sub.apply(frame)
            
            # Clean up the mask
            fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)[1]
            fg_mask = cv2.dilate(fg_mask, None, iterations=2)
            
            # Find contours
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            motion_detected = False
            
            for contour in contours:
                if cv2.contourArea(contour) > self.min_area:
                    motion_detected = True
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if motion_detected and (time.time() - self.last_alert > self.cooldown):
                self.last_alert = time.time()
                self._trigger_alert()
            
            # Optional: Show debug window (remove in production)
            # cv2.imshow(f"Room {self.room_code}", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            time.sleep(0.03)  # ~30 FPS

    def _trigger_alert(self):
        print(f"🚨 MOTION DETECTED in room {self.room_code}!")
        
        from .models import Alert   # avoid circular import
        from django.utils import timezone
        
        try:
            ret, frame = self.cap.read()
            image_path = None
            
            if ret:
                timestamp = int(time.time())
                filename = f"alert_{self.room_code}_{timestamp}.jpg"
                save_path = os.path.join(settings.MEDIA_ROOT, 'alerts', filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                cv2.imwrite(save_path, frame)
                image_path = f"alerts/{filename}"
            
            Alert.objects.create(
                room_id=self.room_code,  # Wait, better use Room object
                # Fix: pass room when creating detector or get by code
                message="Baby movement detected",
                image=image_path
            )
        except Exception as e:
            print("Alert creation failed:", e)