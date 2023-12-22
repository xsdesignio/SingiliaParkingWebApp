from flask import Flask, send_file, render_template, request, session
from flask_cors import CORS
from auth.controllers.login import login_required

from auth.auth_blueprint import auth_bp
from services.users.users_blueprint import users_bp
from services.tickets.tickets_blueprint import tickets_bp
from services.bulletins.bulletins_blueprint import bulletins_bp
from services.zones.zones_blueprint import zones_bp
from services.reports.reports_blueprint import reports_bp

from services.resumeController import get_resume_information
from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
import os


app = Flask(__name__, static_folder='static', template_folder='templates')


cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks=8)
app.secret_key = os.environ.get('FLASK_APP_SECRET_KEY')


app.register_blueprint(auth_bp, url_prefix ='/auth')
app.register_blueprint(tickets_bp, url_prefix ='/tickets')
app.register_blueprint(users_bp, url_prefix ='/users')
app.register_blueprint(bulletins_bp, url_prefix="/bulletins")
app.register_blueprint(zones_bp, url_prefix="/zones")
app.register_blueprint(reports_bp, url_prefix="/reports")


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.get('/')
@login_required
def home():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    request_zone = request.args.get('zone')

    if end_date is not None and end_date != '':
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now()

    if start_date is not None and start_date != '':
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = datetime.now() - timedelta(days=30)

    zone: Zone
    if not (request_zone == 'all' or request_zone == None):
        zone = ZoneModel.get_zone_by_name(request_zone)
    else:
        zone = None

    info = get_resume_information(start_date, end_date, zone)

    start_date = start_date.strftime('%d-%m-%Y')
    end_date = end_date.strftime('%d-%m-%Y')


    zones = ZoneModel.get_zones_list()
    

    return render_template('index.html', start_date = start_date, end_date = end_date, zone = zone, info = info, available_zones = zones)




@app.get("/printer-logo")
@login_required
def printerLogo():
    imageUrl = "./static/assets/mobile/logos.bmp"

    return send_file(imageUrl, mimetype='image/jpeg')

if __name__ == "__main__":
    host = os.environ.get('HOST', 'localhost')
    port = os.environ.get('PORT', 5000)
    app.run(host=host,port=port)
    
