from flask import *
import requests

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
    return r

def parse_weather_response(json_data):
    result = {
        'Temp': json_data['main']['temp'],
        'Humidity': json_data['main']['humidity'],
        'W_speed': json_data['wind']['speed'],
        'Desc' : json_data['weather']['description'],
        'weather_id' :json_data['weather']['id'],
        'pic_id' : json_data['weather']['icon']
    }
    return result

def check_weather(result):
    id = result['weather_id']
    if id in list(range(200, 233)) or True:
        pass

def parse_pic(id):
    pass
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
            weather = {'cityA': resultA, 'cityB': resultB}
        else:
            weather = {'error': 'Не удалось получить данные о погоде.'}
    else:
        return render_template('main.html', weather='sdsdsd')

    return render_template('main.html', weather=weather)
  

if __name__ == '__main__':
    app.run(debug=True)