from flask import Blueprint, render_template, request, jsonify
from auth.controllers.login import login_required

from .models.bulletin_model import BulletinModel
from .entities.bulletin import Bulletin
from .controllers.bulletins_controller import get_bulletins_attributes_count

from services.users.models.user_model import UserModel
from services.utils.payment_methods import PaymentMethod

from services.zones.entities.zone import Zone
from services.zones.models.zone_model import ZoneModel
from services.utils.data_management import parse_date, get_queries_from_request_data, get_range_from_page

from datetime import datetime, timedelta


bulletins_bp = Blueprint('bulletins', __name__, url_prefix='/bulletins', template_folder='./templates')



@bulletins_bp.get('/')
@login_required
def bulletins_page():
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    
    start_date = parse_date(request.args.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(request.args.get('end_date'), datetime.now())
    
    request_zone = request.args.get('zone')

    zone = None
    if request_zone != 'all':
        zone = ZoneModel.get_zone_by_name(request_zone)

    all_bulletins_count = get_bulletins_attributes_count(start_date, end_date)

    # Convert dates to string in order to pass them to the template
    start_date = start_date.strftime('%d-%m-%Y')
    end_date = end_date.strftime('%d-%m-%Y')
    zones = ZoneModel.get_zones_list()

    return render_template('bulletins.html', start_date = start_date, end_date = end_date, bulletins_data = all_bulletins_count, available_zones = zones, zone = zone)




@bulletins_bp.get('/get-bulletin/<id>')
@login_required
def get_bulletin(id: int):
    bulletin = BulletinModel.get_bulletin(id)
    if bulletin != None:
        return jsonify(bulletin.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo el boletin indicado'}, 500


@bulletins_bp.post('/get-bulletins/<page>')
@login_required
def get_bulletins_by_page(page = 0):

    # Getting and preparing the data
    bulletins_range = get_range_from_page(int(page))

    query_values = None

    if(request.content_type == 'application/json') and (request.json != None):
        query_values = get_queries_from_request_data(request.json)


    # Get tickets from database
    bulletins_json = BulletinModel.get_bulletins(bulletins_range, **query_values)

    # Return the tickets as JSON
    if bulletins_json is not None:
        return jsonify(bulletins_json), 200
    else:
        return jsonify({'message': 'Ha ocurrido un error obteniendo los boletines, inténtelo de nuevo más tarde'}), 500



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

    zone: Zone = ZoneModel.get_zone_by_name(bulletin_json["zone_name"])

    payment_method_used = bulletin_json.get('payment_method')

    payment_method:PaymentMethod

    if(payment_method_used == None):
        payment_method = None
    else:
        payment_method= PaymentMethod.get_enum_value(payment_method_used)

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

        bulletin = BulletinModel.get_bulletin(bulletin_id)

        if not bulletin:
            return jsonify({'message': "El boletin que se ha intentado pagar no existe"}), 400
        
        payment_method = request.form.get('payment_method')

        if not payment_method:
            payment_method_used = None
        else:
            payment_method_used = PaymentMethod.get_enum_value(payment_method)

        if not payment_method_used:
            return jsonify({'message': "El metodo de pago indicado no existe"}), 400
        else:
            BulletinModel.pay_bulletin(bulletin_id, payment_method_used)
        
        return jsonify({'message': 'El boletin ha sido pagado con exito'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 400