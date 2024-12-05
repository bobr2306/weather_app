from flask import *
import requests
import os 
from flask import send_from_directory    
 
app = Flask(__name__)


def get_weather(city):
    try:
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
            return {'error': 'Город не найден'}
        elif r.status_code != 200:
            return {'error': 'Ошибка при получении данных о погоде'}
        r.raise_for_status()
        return r
    except requests.RequestException:
        return {'error': 'Ошибка при подключении к сервису погоды'}
    except Exception as e:
        return {'error': f'Произошла непредвиденная ошибка: {str(e)}'}

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
    temp = result['temp']
    wind = result['W_speed']
    water = result['humidity']
    if id in list(range(200, 233)) or id in list(range(502, 532)) or id in list(range(602, 623)) or id in list(range(701, 782)) or temp >= 40 or temp < -10 or wind > 15 or water > 95:
        return "Плохая погода"
    elif id in list(range(300, 322)) or id in list(range(500, 502)) or id in list(range(600, 602)) or wind > 5 or temp < 10:
        return "Нормальная погода"
    elif id == 800 :
        return "Отличная погода"
    else:
        return "Отличная погода"


@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        cityA = request.form.get('departureCity')
        cityB = request.form.get('arrivalCity')
        weather = {}
        if cityA and cityB:
            weatherA = get_weather(cityA)
            weatherB = get_weather(cityB)
            
            if 'error' in weatherA or 'error' in weatherB:
                weather = {'error': weatherA.get('error') if 'error' in weatherA else weatherB.get('error')}
            else:
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
            return render_template('main.html', weather=weather)
    return render_template('main.html', weather=0)

if __name__ == '__main__':
    app.run(debug=True)