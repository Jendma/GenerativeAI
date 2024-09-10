import cv2
import numpy as np
from ultralytics import YOLO
import time
import tkinter as tk
from tkinter import filedialog, messagebox

class PeopleCounterAlert:
    def __init__(self, model_path, max_people, alert_duration):
        # Initialize YOLO model
        self.model = YOLO(model_path)
        # Maximum number of people before alert
        self.max_people = max_people
        # Minimum duration to trigger alert (in seconds)
        self.alert_duration = alert_duration
        # Frame counter for FPS calculation
        self.frame_count = 0
        # Start time for FPS calculation
        self.start_time = time.time()
        # Dictionary to track detected objects
        self.object_tracker = {}
        # Next ID for object labeling
        self.next_id = 1

    def process_frame(self, frame):
        # Increment frame counter
        self.frame_count += 1
        # Get frame dimensions
        height, width = frame.shape[:2]
        # Define monitoring zone (entire frame)
        zone_region = [(0, 0), (width, 0), (width, height), (0, height)]
        
        # Run YOLO detection and tracking
        results = self.model.track(source=frame, classes=[0], persist=True, tracker=r'C:\Users\DSGroupUI\OneDrive - UNIVERSITAS INDONESIA\Documents (1)\Github\GenerativeAI\Tracking and Counting People\custom_track.yaml')
        
        objects_in_zone = []
        current_time = time.time()

        if results[0].boxes.id is not None:
            # Extract bounding box and ID information
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy()

            for box, id in zip(boxes, ids):
                # Extract bounding box coordinates
                x1, y1, x2, y2 = box
                # Calculate object center point
                center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2

                # Check if object is within the zone
                if self.point_in_polygon((center_x, center_y), zone_region):
                    # Initialize or update object information
                    if id not in self.object_tracker:
                        self.object_tracker[id] = {
                            'first_seen': current_time,
                            'label': f"Person {self.next_id}",
                            'persistent': False
                        }
                        self.next_id += 1
                    
                    # Update last seen time of the object
                    self.object_tracker[id]['last_seen'] = current_time
                    # Mark object as persistent if seen long enough
                    if current_time - self.object_tracker[id]['first_seen'] >= self.alert_duration:
                        self.object_tracker[id]['persistent'] = True
                    
                    objects_in_zone.append(id)
                    
                    # Draw bounding box and label
                    color = (0, 0, 255) if not self.object_tracker[id]['persistent'] else (255, 0, 0)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(frame, self.object_tracker[id]['label'], (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Count persistent objects
        persistent_objects = [obj for obj in objects_in_zone if self.object_tracker[obj]['persistent']]
        
        # Draw monitoring zone
        cv2.polylines(frame, [np.array(zone_region, np.int32)], True, (255, 0, 0), 2)
        
        # Calculate and display FPS
        if self.frame_count % 30 == 0:
            fps = 30 / (current_time - self.start_time)
            self.start_time = current_time
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display number of people in zone
        cv2.putText(frame, f"People in zone: {len(objects_in_zone)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display alert if number of persistent people exceeds threshold
        if len(persistent_objects) >= self.max_people:
            cv2.putText(frame, "ALERT: Too many people!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return frame

    def point_in_polygon(self, point, polygon):
        # Implementation of ray-casting algorithm to determine if a point is inside a polygon
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def run(self, source):
        if isinstance(source, str) and source.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Process static image
            frame = cv2.imread(source)
            processed_frame = self.process_frame(frame)
            cv2.imshow("People Counter and Alert System", processed_frame)
            cv2.waitKey(0)
        else:
            # Process video or camera stream
            cap = cv2.VideoCapture(source)
            
            while cap.isOpened():
                success, frame = cap.read()
                if success:
                    processed_frame = self.process_frame(frame)
                    cv2.imshow("People Counter and Alert System", processed_frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break

            cap.release()
        
        cv2.destroyAllWindows()

def select_source():
    # Create hidden Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Display dialog to choose input source
    source_type = messagebox.askquestion("Input Selection", "Do you want to use a camera stream?")
    
    if source_type == 'yes':
        return 0  # Use default camera
    else:
        # Open dialog to select file
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image/Video files", "*.png *.jpg *.jpeg *.mp4 *.avi *.mov"),
            ("All files", "*.*")
        ])
        return file_path if file_path else None

def main():
    # Path to YOLO model
    model_path = r"C:\Users\DSGroupUI\OneDrive - UNIVERSITAS INDONESIA\Documents (1)\Github\GenerativeAI\Tracking and Counting People\yolov10b.pt"
    # Maximum number of people before alert
    max_people = 4
    # Duration to trigger alert (in seconds)
    alert_duration = 120  # 2 minutes

    # Select input source
    source = select_source()
    if source is None:
        print("No source selected. Exiting.")
        return

    # Create and run PeopleCounterAlert instance
    counter = PeopleCounterAlert(model_path, max_people, alert_duration)
    counter.run(source)

if __name__ == "__main__":
    main()