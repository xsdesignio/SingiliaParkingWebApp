from flask import Flask, render_template, request
from flask_cors import CORS
from auth.controllers.login import login_required

from auth.auth_blueprint import auth_bp
from services.users.users_blueprint import users_bp
from services.tickets.tickets_blueprint import tickets_bp
from services.bulletins.bulletins_blueprint import bulletins_bp
from services.zones.zones_blueprint import zones_bp

from services.resumeController import get_resume_information

from datetime import datetime, timedelta


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
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    zone_name = request.args.get('zone')

    if end_date is not None and end_date != '':
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now()

    if start_date is not None and start_date != '':
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = datetime.now() - timedelta(days=30)

    if zone_name == 'all':
        zone_name = None


    info = get_resume_information(start_date, end_date, zone_name)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    return render_template('index.html', start_date = start_date, end_date = end_date, zone = zone_name, info = info)




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    
