from flask import Blueprint, render_template, request, jsonify
from auth.controllers.login import login_required

from .models.bulletin_model import BulletinModel
from .entities.bulletin import Bulletin
from .controller.bulletins_controller import get_bulletins_attributes_counter

from services.users.models.user_model import UserModel
from services.utils.payment_methods import PaymentMethod

from services.zones.entities.zone import Zone

from datetime import datetime, timedelta


bulletins_bp = Blueprint('bulletins', __name__, url_prefix='/bulletins', template_folder='./templates')



@bulletins_bp.get('/')
@login_required
def bulletins_page():
    """ Returns the bulletins filtered by date or by location. Filters are optional and can be combined. They are obtained by get arguments."""
    
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

    if location == 'all':
        location = None
        


    zone: Zone = Zone.get_zone_by_name(request_zone)
    bulletins = BulletinModel.get_bulletins_by_filter(start_date, end_date, zone)



    count_all_bulletins = BulletinModel.get_bulletins_attributes_counter(start_date, end_date, zone)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    return render_template('bulletins.html', bulletins=bulletins, start_date=start_date, end_date=end_date, location=location, bulletins_data = count_all_bulletins)



@bulletins_bp.get('/get-bulletin/<id>')
@login_required
def get_bulletin(id: int):
    bulletin = BulletinModel.get_bulletin(id)
    if bulletin != None:
        return jsonify(bulletin.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo el boletin indicado'}, 500


@bulletins_bp.get('/get-bulletins')
@login_required
def get_bulletins():
    bulletin_json = BulletinModel.get_bulletins()
    if bulletin_json != None:
        return jsonify(bulletin_json), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo los boletines, initéntelo de nuevo más tarde'}, 500


@bulletins_bp.post('/create/')
@login_required
def create_bulletin():
    bulletin_json = request.get_json()
    bulletin: Bulletin

    responsible = UserModel.get_user(bulletin_json['responsible_id'])
    zone = Zone.get_zone(bulletin_json["zone_id"])
    payment_method = PaymentMethod(bulletin_json["payment_method"])


    try:
        bulletin = BulletinModel.create_bulletin(
            responsible = responsible, 
            zone = zone, 
            duration = bulletin_json['duration'], 
            registration = bulletin_json['registration'], 
            price = bulletin_json['price'],  
            payment_method = payment_method,
            paid = bulletin_json['paid'],  
            created_at = bulletin_json['created_at'] or None,
            brand = bulletin_json.get("brand"), 
            model = bulletin_json.get("model"), 
            color = bulletin_json.get("color"),)
        
    except Exception as exception:
        print(exception)
        return {'message': 'El boletin no pudo ser creado en la base de datos.'}, 400


    if bulletin != None:
        bulletin_data: dict = bulletin.to_json()
        return jsonify(bulletin_data), 200
    else:
        return {'message': 'Ha ocurrido un error inesperado.'}, 500
    


@bulletins_bp.post('/pay/<id>')
@login_required
def pay_bulletin(id: int):
    try:
        bulletin_id = int(id)

        if(BulletinModel.get_bulletin(bulletin_id) == None):
            return jsonify({'message': "El boletin que se ha intentado pagar no existe"}), 400
        
        BulletinModel.pay_bulletin(bulletin_id)

        return jsonify({'message': 'El boletin ha sido pagado con exito'}), 200
    except Exception as e:
        return jsonify({'message': e.__str__()}), 400


