import json

# Load detection_results.json
with open("detection_results.json", "r") as file:
    detections = json.load(file)

occupied_detections = [d for d in detections if d["class_id"] == 0]

print(f"🔍 Total Occupied Detections: {len(occupied_detections)}")
print(json.dumps(occupied_detections, indent=4))
