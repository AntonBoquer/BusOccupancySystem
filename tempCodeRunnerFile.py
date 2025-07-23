import json
import numpy as np

def load_detection_results(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def assign_seat_numbers(detections, seat_labels):
    seat_detections = [d for d in detections if d['class_name'] in ['Occupied', 'Unoccupied']]
    seat_detections.sort(key=lambda d: (d['y_min'], d['x_min']))
    
    row_threshold = 40
    rows = []
    for seat in seat_detections:
        placed = False
        for row in rows:
            if abs(row[0]['y_min'] - seat['y_min']) < row_threshold:
                row.append(seat)
                placed = True
                break
        if not placed:
            rows.append([seat])
    
    for row in rows:
        row.sort(key=lambda d: d['x_min'])
    
    seat_map = {}
    seat_number = 0  
    for row in rows:
        for seat in row:
            if seat_number < len(seat_labels):
                seat_status = 1 if seat['class_name'] == 'Unoccupied' else 0
                seat_map[seat_labels[seat_number]] = seat_status
                seat_number += 1
    
    return seat_map

seats = [
    "tenone", "tentwo", "tenthree", "tenfour", "tenfive",
    "nineone", "ninetwo",
    "eightone", "eighttwo", "eightthree", "eightfour",
    "sevenone", "seventwo", "seventhree", "sevenfour",
    "sixone", "sixtwo", "sixthree", "sixfour",
    "fiveone", "fivetwo", "fivethree", "fivefour",
    "fourone", "fourtwo", "fourthree", "fourfour",
    "threeone", "threetwo", "threethree", "threefour",
    "twoone", "twotwo", "twothree", "twofour",
    "oneone", "onetwo", "onethree", "onefour"
]


detections = load_detection_results('detection_results.json')
seat_positions = assign_seat_numbers(detections, seats)

# Write results to a JSON file
with open('seat_positions.json', 'w') as outfile:
    json.dump(seat_positions, outfile, indent=4)

print(json.dumps(seat_positions, indent=4))
