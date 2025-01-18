import pyautogui
import cv2
import numpy as np
from PIL import Image
from threading import Thread, Event
import time

class ScreenCapture:
    def __init__(self):
        self.running = False
        self.stop_event = Event()
        self.capture_thread = None
        self.frame_callback = None
        self.fps = 30
        
    def start(self, fps=30, callback=None):
        """Start screen capture with specified FPS"""
        self.fps = fps
        self.frame_callback = callback
        self.running = True
        self.stop_event.clear()
        self.capture_thread = Thread(target=self._capture_loop)
        self.capture_thread.start()
        
    def stop(self):
        """Stop screen capture"""
        self.running = False
        self.stop_event.set()
        if self.capture_thread:
            self.capture_thread.join()
            
    def _capture_loop(self):
        """Main capture loop"""
        while self.running:
            start_time = time.time()
            
            # Capture screen
            screenshot = pyautogui.screenshot()
            
            # Convert to numpy array
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Send frame to callback if registered
            if self.frame_callback:
                self.frame_callback(frame)
                
            # Calculate sleep time to maintain FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, 1.0/self.fps - elapsed)
            time.sleep(sleep_time)
            
            if self.stop_event.is_set():
                break
