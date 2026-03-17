from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "cf1b23d89b80bb744ab2b99d3b2750c3"

# 🌦️ Main Route
@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = []

    if request.method == 'POST':
        city = request.form['city']

        # Current Weather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather = {
                "city": city,
                "temp": data["main"]["temp"],
                "desc": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "icon": data["weather"][0]["icon"]
            }

            # 📅 Forecast
            f_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            f_response = requests.get(f_url)
            f_data = f_response.json()

            for item in f_data["list"][:5]:
                forecast.append({
                    "temp": item["main"]["temp"],
                    "icon": item["weather"][0]["icon"]
                })

        else:
            weather = {
                "city": city,
                "temp": "--",
                "desc": "Invalid city",
                "humidity": "--"
            }

    return render_template("index.html", weather=weather, forecast=forecast)


# 📍 Location Route (NEW FEATURE)
@app.route('/location', methods=['GET', 'POST'])
def location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    weather = None
    forecast = []

    # Current Weather using location
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        weather = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "icon": data["weather"][0]["icon"]
        }

        # 📅 Forecast using location
        f_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        f_response = requests.get(f_url)
        f_data = f_response.json()

        for item in f_data["list"][:5]:
            forecast.append({
                "temp": item["main"]["temp"],
                "icon": item["weather"][0]["icon"]
            })

    else:
        weather = {
            "city": "Unknown",
            "temp": "--",
            "desc": "Error fetching location weather",
            "humidity": "--"
        }

    return render_template("index.html", weather=weather, forecast=forecast)


# ▶️ Run App
if __name__ == "__main__":
    app.run(debug=True)