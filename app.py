from flask import Flask, render_template
from flask_cors import CORS
from auth.controllers.login import login_required

from auth.auth_blueprint import auth_bp
from services.users.users_blueprint import users_bp
from services.tickets.tickets_blueprint import tickets_bp
from services.bulletins.bulletins_blueprint import bulletins_bp
from services.zones.zones_blueprint import zones_bp


app = Flask(__name__, static_folder='static', template_folder='templates')


cors = CORS(app, resources={r"/*": {"origins": "*"}})


app.secret_key = 'tu_clave_secreta_aqui'

host = 'localhost'
port = '5432'

app.register_blueprint(auth_bp, url_prefix ='/auth')
app.register_blueprint(tickets_bp, url_prefix ='/tickets')
app.register_blueprint(users_bp, url_prefix ='/users')
app.register_blueprint(bulletins_bp, url_prefix="/bulletins")
app.register_blueprint(zones_bp, url_prefix="/zones")


@app.get('/')
@login_required
def home():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
