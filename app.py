from flask import Flask
from flask_cors import CORS

from api.auth_blueprint import auth_bp
from api.users_blueprint import users_bp
from api.tickets_blueprint import tickets_bp


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "exp://192.168.1.39:19000"}})

app.secret_key = 'tu_clave_secreta_aqui'

host = 'localhost'
port = '5432'

app.register_blueprint(auth_bp, url_prefix ='/auth')
app.register_blueprint(tickets_bp, url_prefix ='/tickets')
app.register_blueprint(users_bp, url_prefix ='/users')


@app.get('/')
def home():
    return f'<h1>Result should be 2 -> result:</h1>'




if __name__ == "__main__":
    app.run(host='192.168.1.39', port=5000)
