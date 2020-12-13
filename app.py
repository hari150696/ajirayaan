from flask import Flask
from routes.environment import Environment
from routes.rover import Rover

app = Flask(__name__)
app.register_blueprint(Environment)
app.register_blueprint(Rover)

if __name__ == '__main__':
    app.run(debug=True)
