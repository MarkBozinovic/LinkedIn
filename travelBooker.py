from flask import Flask, request, jsonify, render_template
import openai
import datetime

app = Flask(__name__)
openai.api_key = "API-KEY"  # Replace with your real API key

# Simulated databases
FLIGHTS_DB = [
    {"flight_id": 1, "from": "Melbourne", "to": "Tokyo", "date": "2025-06-01", "price": 850},
    {"flight_id": 2, "from": "Melbourne", "to": "Sydney", "date": "2025-06-05", "price": 120},
]

HOTELS_DB = [
    {"hotel_id": 1, "city": "Tokyo", "name": "Tokyo Grand", "price_per_night": 120},
    {"hotel_id": 2, "city": "Sydney", "name": "Harbour View", "price_per_night": 180},
]

# Homepage
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Plan trip from form
@app.route("/plan_form", methods=["POST"])
def plan_form():
    user_data = request.form
    prompt = (
        f"Plan a holiday based on the following:\n"
        f"Travel dates: {user_data.get('travel_dates')}\n"
        f"From: {user_data.get('from')}\n"
        f"To: {user_data.get('to')}\n"
        f"Preferences: {user_data.get('preferences')}\n"
        f"Activities: {user_data.get('activities')}\n"
        f"Accommodation type: {user_data.get('accommodation')}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    itinerary = response.choices[0].message["content"].strip()

    return render_template("index.html", itinerary=itinerary)

# Flights search API
@app.route("/search_flights", methods=["POST"])
def search_flights():
    data = request.json
    flights = [f for f in FLIGHTS_DB if f['from'] == data['from'] and f['to'] == data['to']]
    return jsonify(flights)

# Hotels search API
@app.route("/search_hotels", methods=["POST"])
def search_hotels():
    data = request.json
    hotels = [h for h in HOTELS_DB if h['city'] == data['to']]
    return jsonify(hotels)

# Booking API
@app.route("/book", methods=["POST"])
def book():
    details = request.json
    confirmation = {
        "booking_id": f"BK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "flight_id": details.get("flight_id"),
        "hotel_id": details.get("hotel_id"),
        "status": "confirmed"
    }
    return jsonify(confirmation)

# Travel alerts
@app.route("/travel_alerts", methods=["GET"])
def travel_alerts():
    return jsonify({
        "Japan": "Avoid northern Honshu due to recent earthquake.",
        "France": "Nationwide strikes may disrupt travel services.",
        "Indonesia": "Monitor volcanic activity alerts for Bali."
    })

if __name__ == "__main__":
    app.run(debug=True)
