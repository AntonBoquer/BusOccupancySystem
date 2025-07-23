import json
import numpy as np
import time
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load predefined seat bounding boxes from your data
seat_boxes = {
    "oneone": {"x": 422.67, "y": 836.10, "width": 332.39, "height": 428.82},
    "onetwo": {"x": 790.00, "y": 872.50, "width": 380.00, "height": 575.00},
    "onethree": {"x": 1755.00, "y": 810.00, "width": 360.00, "height": 650.00},
    "onefour": {"x": 2095.00, "y": 805.00, "width": 300.00, "height": 620.00},
    "twoone": {"x": 621.17, "y": 494.92, "width": 255.35, "height": 169.28},
    "twotwo": {"x": 906.64, "y": 482.01, "width": 275.44, "height": 183.62},
    "twothree": {"x": 1641.14, "y": 400.24, "width": 263.96, "height": 169.28},
    "twofour": {"x": 1896.49, "y": 410.28, "width": 223.79, "height": 149.19},
    "threeone": {"x": 750.53, "y": 339.55, "width": 202.25, "height": 89.06},
    "threetwo": {"x": 985.25, "y": 330.27, "width": 211.52, "height": 103.91},
    "threethree": {"x": 1562.30, "y": 273.68, "width": 178.12, "height": 79.78},
    "threefour": {"x": 1763.62, "y": 283.89, "width": 187.40, "height": 81.64},
    "fourone": {"x": 833.30, "y": 251.75, "width": 166.99, "height": 66.80},
    "fourtwo": {"x": 1033.73, "y": 240.60, "width": 170.91, "height": 64.71},
    "fourthree": {"x": 1502.89, "y": 199.11, "width": 143.53, "height": 58.07},
    "fourfour": {"x": 1674.63, "y": 209.90, "width": 145.19, "height": 54.76},
    "fiveone": {"x": 903.89, "y": 187.91, "width": 136.89, "height": 48.95},
    "fivetwo": {"x": 1071.48, "y": 184.18, "width": 138.55, "height": 39.82},
    "fivethree": {"x": 1465.56, "y": 144.36, "width": 125.28, "height": 38.16},
    "fivefour": {"x": 1610.33, "y": 157.63, "width": 126.11, "height": 44.80},
    "sixone": {"x": 948.28, "y": 145.60, "width": 119.47, "height": 25.72},
    "sixtwo": {"x": 1086.41, "y": 142.28, "width": 120.30, "height": 35.67},
    "sixthree": {"x": 1431.54, "y": 111.17, "width": 100.39, "height": 26.55},
    "sixfour": {"x": 1556.41, "y": 119.88, "width": 92.92, "height": 22.40},
    "sevenone": {"x": 973.17, "y": 123.62, "width": 97.90, "height": 26.55},
    "seventwo": {"x": 1097.61, "y": 114.49, "width": 104.53, "height": 26.55},
    "seventhree": {"x": 1406.24, "y": 87.53, "width": 94.58, "height": 22.40},
    "sevenfour": {"x": 1521.56, "y": 91.68, "width": 86.28, "height": 25.72},
    "eightone": {"x": 1022.53, "y": 94.16, "width": 87.11, "height": 37.33},
    "eighttwo": {"x": 1130.39, "y": 83.38, "width": 90.43, "height": 30.70},
    "eightthree": {"x": 1388.40, "y": 50.19, "width": 83.79, "height": 38.99},
    "eightfour": {"x": 1488.38, "y": 50.19, "width": 84.62, "height": 45.63},
    "nineone": {"x": 1040.78, "y": 59.73, "width": 85.45, "height": 31.53},
    "ninetwo": {"x": 1144.49, "y": 54.34, "width": 83.79, "height": 30.70},
    "tenone": {"x": 1092.22, "y": 18.25, "width": 83.79, "height": 36.50},
    "tentwo": {"x": 1177.67, "y": 17.84, "width": 75.50, "height": 35.67},
    "tenthree": {"x": 1277.65, "y": 71.76, "width": 86.28, "height": 143.53},
    "tenfour": {"x": 1373.47, "y": 14.10, "width": 80.48, "height": 28.21},
    "tenfive": {"x": 1458.51, "y": 14.10, "width": 79.65, "height": 28.21}
}
# Compute seat midpoints
# seat_midpoints = {seat: (box["x"] + box["width"] / 2, box["y"] + box["height"] / 2) for seat, box in seat_boxes.items()}
seat_midpoints = {seat: (box["x"], box["y"]) for seat, box in seat_boxes.items()}



# ✅ Step 4: Function to Read Detection Results
def read_detection_results():
    try:
        with open("detection_results6.json", "r") as file:
            seat_data = json.load(file)
            print(f"Loaded Detection Data: {json.dumps(seat_data, indent=2)}")  # Debug log
            return seat_data    
    except FileNotFoundError:
        print("Error: detection_results6.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in detection_results6.json!")
        return []



# previous_seat_status = {} 
# ✅ Step 5: Function to Process and Update Seats
# previous_seat_status = {} 

# Step 1: Iterate through detections and process only occupied seats
# ✅ Function to Process and Update Seats in Supabase
def process_and_update_seats():
    detections = read_detection_results()  


    occupied_seats = {}  # Store detected occupied seats


    for detection in detections:
        if detection["class_id"] != 0:  # 0 means occupied
            continue  # Skip unoccupied seats

        x_center = (detection["x_min"] + detection["x_max"]) / 2
        y_center = (detection["y_min"] + detection["y_max"]) / 2

        assigned_seat = None
        min_distance = float("inf")  # Initialize with a large number

        for seat, box in seat_boxes.items():
            # x1, y1 = box["x"], box["y"]
            # x2, y2 = x1 + box["width"], y1 + box["height"]
            x1, y1 = box["x"] - box["width"]/2, box["y"] - box["height"]/2
            x2, y2 = box["x"] + box["width"]/2, box["y"] + box["height"]/2

            if x1 <= x_center <= x2 and y1 <= y_center <= y2:
                if seat not in occupied_seats:  # ✅ Prevent duplicate assignments
                    occupied_seats[seat] = 0
                    print(f"🪑 Assigned Seat: {seat}")  # Debug print
                break  # ✅ Stop checking after the first valid match

            # If not inside, assign the closest seat
            seat_mid_x, seat_mid_y = seat_midpoints[seat]
            distance = ((x_center - seat_mid_x) ** 2 + (y_center - seat_mid_y) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                assigned_seat = seat  # ✅ Assign closest seat

        if assigned_seat:
            occupied_seats[assigned_seat] = 0  # Mark as occupied
            print(f"🪑 Assigned Seat: {assigned_seat}") 
        else:
            print(f"⚠️ No seat found for detection at ({x_center}, {y_center})")



    # ✅ Step 2: Get all seat statuses from Supabase
    response = supabase.table("seats").select("seat_number", "status").execute()
    all_seats = {seat["seat_number"]: seat["status"] for seat in response.data}  # Get existing status

    # ✅ Step 3: Update seat statuses
    seat_status = {seat: occupied_seats.get(seat, 1) for seat in seat_boxes}  # Default to unoccupied

    print(f"📌 Updated Seat Status Before DB Update: {seat_status}")  # Debug print

    # ✅ Step 4: Update Supabase
    for seat, status in seat_status.items():
        response = (
            supabase.table("seats")
            .update({"status": bool(status == 1)})  # Convert 0 (occupied) to False
            .eq("seat_number", seat) 
            .execute()
        )
        print(f"✅ Updated seat {seat}: {response}")  # Debug print



# ✅ Step 6: Run the update function in a loop every 5 seconds
# previous_seat_status = {}  # Store the last known seat statuses to avoid unnecessary updates

# File system event handler
class DetectionResultsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """Triggered when the file is modified."""
        if event.src_path.endswith("detection_results6.json"):
            print("🔄 Changes detected in detection_results6.json. Processing updates...")
            process_and_update_seats()

# Set up the file system observer
def start_file_monitoring():
    event_handler = DetectionResultsHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)  # Monitor the current directory
    observer.start()
    print("🔍 Monitoring detection_results6.json for changes...")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start monitoring for changes
start_file_monitoring()




# # Print final seat occupancy
# print("\n🪑 Final Seat Status:")
# print(json.dumps(seat_status, indent=4))    
# print(f"📄 Loaded Detection Data: {json.dumps(seat_data, indent=2)}")  # Debug log

# print(f"📌 Final Detected Occupied Seats: {occupied_seats}")  # Should NOT be empty
# print(f"📌 Updated Seat Status Before DB Update: {seat_status}")  # Should have True/False values
