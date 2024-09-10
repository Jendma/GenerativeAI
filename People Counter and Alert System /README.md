# People Counter and Alert System

## High-Level Approach/Architecture

This system is designed to count the number of people in a specified area and issue an alert when the number of people exceeds a certain threshold for a defined period. The system architecture consists of several key components:

1. Object Detection and Tracking: Utilizes the YOLO model to detect and track people in video frames.
2. Zone Definition: Defines a monitoring zone within the frame.
3. People Counting: Counts the number of people detected within the specified zone.
4. Persistence Tracking: Tracks the presence of people in the zone over a specified time period.
5. Alert System: Triggers an alert when defined conditions are met.
6. Visualization: Displays detection results, tracking, and alerts on the video frame.

## Tech Stack

- Python: Primary programming language
- OpenCV (cv2): For image and video processing
- Ultralytics YOLO: For object detection and tracking
- NumPy: For numerical and array operations
- Tkinter: For a simple user interface in input source selection

## Implementation Steps

1. Initialization:
   - Load the YOLO model
   - Set parameters for maximum number of people and alert duration

2. Frame Processing:
   - Run YOLO detection and tracking on each frame
   - Determine if detected objects are within the specified zone
   - Track persistent objects in the zone

3. Counting and Alerting:
   - Count the number of people in the zone
   - Trigger an alert if the number of people exceeds the threshold for the specified duration

4. Visualization:
   - Draw bounding boxes for each detected person
   - Display information such as people count and alert status

5. Input Handling:
   - Provide options to choose between camera stream or video/image file as input

6. Main Loop:
   - Process frames sequentially from the chosen input source
   - Display processing results in real-time

## Usage

1. Install all required libraries in Terminal
   ```
   pip install -r requirements.txt
   ```
3. Run the main script in Terminal
   ```
   python tracker.py  
   ```
4. Select the input source (camera or file)
5. The system will start counting and monitoring
6. An alert will appear if the specified conditions are met

## Customization

The system can be customized by modifying parameters such as:
- Maximum number of allowed people
- Duration to trigger an alert
- Definition of the monitoring zone
- Byte Track parameter
