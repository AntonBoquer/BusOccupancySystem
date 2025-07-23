import subprocess
import json
from flask import Flask, jsonify
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


app = Flask(__name__)

# Run seating.py when the server starts
print("🚀 Running seating.py to process detections...")
subprocess.run(["python", "seating.py"], check=True)


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
