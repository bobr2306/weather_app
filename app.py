from flask import *
import requests
import os 
from flask import send_from_directory    
 
app = Flask(__name__)


def get_weather(city):
    api_key = 'eceebf763209c2eaea7c4c70a47ef6bb'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid': api_key,
        'q': city,
        'units': 'metric',
        'lang': 'ru'
    }
    r = requests.get(base_url, params=params)
    if r.status_code == 404:
        return None
    return r

def parse_weather_response(json_data):
    result = {
        'temp': json_data['main']['temp'],
        'humidity': json_data['main']['humidity'],
        'pressure': json_data['main']['pressure'],
        'W_speed': json_data['wind']['speed'],
        'Desc' : json_data['weather'][0]['description'],
        'weather_id' : json_data['weather'][0]['id'],
        'pic_id' : json_data['weather'][0]['icon']
    }
    return result

def check_weather(result):
    id = result['weather_id']
    if id in list(range(200, 233)) or id in list(range(502, 532)) or id in list(range(602, 623)) or id in list(range(701, 782)):
        return "Плохая погода"
    elif id == 800:
        return "Отличная погода"
    elif id in list(range(300, 322)) or id in list(range(500, 502)) or id in list(range(600, 602)):
        return "Средняя погода"
    else:
        return "Нормальная погода"


@app.route('/', methods=['GET'])
def base():
    cityA = request.args.get('departureCity')
    cityB = request.args.get('arrivalCity')
    weather = {}
    if cityA and cityB:
        weatherA = get_weather(cityA)
        weatherB = get_weather(cityB)        
        if weatherA and weatherB:
            resultA = parse_weather_response(weatherA.json())
            resultB = parse_weather_response(weatherB.json())
            weather = {
                'cityA': cityA,
                'cityB': cityB,
                'weather_descriptionA': resultA['Desc'],
                'weather_descriptionB': resultB['Desc'],
                'tempA': resultA['temp'],
                'tempB': resultB['temp'],
                'wind_speedA': resultA['W_speed'],
                'wind_speedB': resultB['W_speed'],
                'humidityA': resultA['humidity'],
                'humidityB': resultB['humidity'],
                'pressureA': resultA['pressure'],
                'pressureB': resultB['pressure'],
                'iconA': resultA['pic_id'],
                'iconB': resultB['pic_id'],
                'detailed_descriptionA': check_weather(resultA),
                'detailed_descriptionB': check_weather(resultB)
            }
        else:
            weather = {'error': 'Не удалось получить данные о погоде.'}
    else:
        return render_template('main.html', weather=0)

    return render_template('main.html', weather=weather)
  

if __name__ == '__main__':
    app.run(debug=True)