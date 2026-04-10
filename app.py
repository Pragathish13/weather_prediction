from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("271372df647acf07335e8ab7c7e6dc69")  # secure key

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form['city']

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "200":
            error = "City not found!"
        else:
            weather = []
            for i in range(0, 40, 8):  # 5-day forecast
                day = data["list"][i]
                weather.append({
                    "date": day["dt_txt"],
                    "temp": day["main"]["temp"],
                    "desc": day["weather"][0]["description"],
                    "icon": day["weather"][0]["icon"]
                })

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)