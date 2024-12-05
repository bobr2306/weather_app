from flask import *
import requests

app = Flask(__name__)

def get_weather(city):
    api_key = 'eceebf763209c2eaea7c4c70a47ef6bb'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid': api_key,
        'q': city,
        'units': 'metric'
    }
    r = request.get(base_url, params=params)
    weather = {
        'rain': r
    }

@app.route('/', methods=['GET'])
def cum():
    if request:
        cityA = request.args.get('departureCity')
        cityB = request.args.get('arrivalCity')
        return render_template('main.html', city=cityA)
    return render_template('main.html', city='')
  

if __name__ == '__main__':
    app.run(debug=True)