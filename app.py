from flask import *

app = Flask(__name__)

@app.route('/')
def cum():
    return('Goall')

if __name__ == '__main__':
    app.run(debug=True)