from flask import Blueprint, render_template, request, jsonify
from auth.controllers.login import login_required

from .models.bulletin_model import BulletinModel
from .entities.bulletin import Bulletin
from .controllers.bulletins_controller import get_bulletins_attributes_count

from services.users.models.user_model import UserModel
from services.utils.payment_methods import PaymentMethod

from services.zones.entities.zone import Zone
from services.zones.models.zone_model import ZoneModel

from datetime import datetime, timedelta


bulletins_bp = Blueprint('bulletins', __name__, url_prefix='/bulletins', template_folder='./templates')



@bulletins_bp.get('/')
@login_required
def bulletins_page():
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    
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

    query_values = {
        "start_date": start_date, 
        "end_date":  end_date, 
    }

    if not (request_zone == 'all' or request_zone == None):
        zone = ZoneModel.get_zone_by_name(request_zone)
        query_values["zone_id"] = zone.id


    bulletins = BulletinModel.get_bulletins(**query_values)

    all_bulletins_count = get_bulletins_attributes_count(start_date, end_date)

    # Convert dates to string in order to pass them to the template
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    zones = ZoneModel.get_zones_list()

    return render_template('bulletins.html', bulletins = bulletins, start_date = start_date, end_date = end_date, bulletins_data = all_bulletins_count, available_zones = zones, zone = request_zone)




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
    """Get all bulletins
    
    Return: json string with all bulletins
    """
    
    bulletin_json = BulletinModel.get_bulletins()
    if bulletin_json != None:
        return jsonify(bulletin_json), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo los boletines, initéntelo de nuevo más tarde'}, 500


@bulletins_bp.post('/create/')
@login_required
def create_bulletin():
    """Create a new bulletin on database from a json dict

    Json arguments on request body:

    responsible_id -- id of the user who created the bulletin
    zone -- zone where the bulletin was created
    duration -- duration of the bulletin in minutes
    registration -- registration of the vehicle
    price -- price of the bulletin
    payment_method -- payment method of the bulletin
    paid -- if the bulletin has been paid
    precept -- precept of the bulletin (Optional)
    created_at -- date when the bulletin was created
    brand -- brand of the vehicle (Optional)
    model -- model of the vehicle (Optional)
    color -- color of the vehicle (Optional)

    Return: json object string with the created bulletin
    """

    bulletin_json = request.get_json()
    bulletin: Bulletin

    responsible = UserModel.get_user(bulletin_json['responsible_id'])

    zone: Zone = ZoneModel.get_zone_by_name(bulletin_json["zone"])

    payment_method:PaymentMethod = PaymentMethod.get_enum_value(bulletin_json.get('payment_method', 'CASH'))


    try:
        bulletin = BulletinModel.create_bulletin(
            responsible = responsible, 
            zone = zone, 
            duration = bulletin_json['duration'], 
            registration = bulletin_json['registration'], 
            price = bulletin_json['price'],  
            payment_method = payment_method,
            paid = bulletin_json['paid'],  
            precept= bulletin_json.get('precept', None),
            created_at = bulletin_json.get('created_at', datetime.now()),
            brand = bulletin_json.get("brand"), 
            model = bulletin_json.get("model"), 
            color = bulletin_json.get("color")
        )
        
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


