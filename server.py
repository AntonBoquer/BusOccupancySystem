import subprocess
import json
from flask import Flask, jsonify
from supabase import create_client

app = Flask(__name__)

# Run seating.py when the server starts
print("🚀 Running seating.py to process detections...")
subprocess.run(["python", "seating.py"], check=True)

# Supabase credentials
SUPABASE_URL = "https://yhsoxuyjrdchmbrlwqci.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inloc294dXlqcmRjaG1icmx3cWNpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEwNzE0MjksImV4cCI6MjA1NjY0NzQyOX0.pSsbZwAG8HNOQ-WPuKaRunoTn-Bal4uqDMlnhupe0DY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/get-seat-positions', methods=['GET'])
def get_seat_positions():
    try:
        response = supabase.table("seats").select("*").execute()
        seat_data = response.data
        return jsonify(seat_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
