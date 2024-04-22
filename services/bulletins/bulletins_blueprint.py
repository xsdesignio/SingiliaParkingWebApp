from decimal import Decimal
from flask import Blueprint, redirect, render_template, request, jsonify, session, url_for, flash
from auth.controllers.login import login_required, role_required
from services.bulletins.entities.available_bulletin import AvailableBulletin
from services.users.controllers.withheld import add_withheld_to_user

from .models.bulletin_model import BulletinModel
from .models.available_bulletin_model import AvailableBulletinModel
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
    """ Returns the bulletins filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    
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




@bulletins_bp.get('/get-bulletin/<path:id>')
@login_required
def get_bulletin(id: str):
    bulletin = BulletinModel.get_bulletin(id)
    
    if bulletin != None:
        return jsonify(bulletin.to_json()), 200
    else:
        return jsonify({}), 200



@bulletins_bp.get('/get-bulletins-by-registration/<path:registration>')
@login_required
def get_bulletin_by_registration(registration: str):
    bulletins_json = BulletinModel.get_bulletins(registration = registration) or []
    return jsonify(bulletins_json), 200



@bulletins_bp.post('/get-bulletins/<page>')
@login_required
def get_bulletins_by_page(page = 0):
    """Get bulletins based on its 'page', the page is used to obtain a range of the bulletins """

    # Getting and preparing the data
    bulletins_range = get_range_from_page(int(page))

    query_values = None

    if(request.content_type == 'application/json') and (request.json != None):
        query_values = get_queries_from_request_data(request.json)


    # Get bulletins from database
    bulletins_json = BulletinModel.get_bulletins(bulletins_range, **query_values)

    # Return the bulletins as JSON
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

    zone -- zone where the bulletin was created
    registration -- registration of the vehicle
    precept -- precept of the bulletin (Optional)
    created_at -- date when the bulletin was created
    brand -- brand of the vehicle (Optional)
    model -- model of the vehicle (Optional)
    color -- color of the vehicle (Optional)

    Return: json object string with the created bulletin
    """

    bulletin_json = request.get_json()
    bulletin: Bulletin

    session_id: int = session.get("id")
    user_id: int = bulletin_json.get("responsible_id", session_id)
    responsible = UserModel.get_user(user_id)

    zone: Zone = ZoneModel.get_zone_by_name(bulletin_json.get("zone_name", None))

    try:
        bulletin = BulletinModel.create_bulletin(
            responsible = responsible, 
            zone = zone, 
            registration = bulletin_json['registration'], 
            precept= bulletin_json.get('precept', None),
            created_at = bulletin_json.get('created_at', datetime.now()),
            brand = bulletin_json.get("brand"), 
            model = bulletin_json.get("model"), 
            color = bulletin_json.get("color")
        )
        
    except Exception as exception:
        print(exception.args[0])
        return {'message': 'El boletin no pudo ser creado en la base de datos.'}, 400


    if bulletin != None:
        bulletin_data: dict = bulletin.to_json()
        return jsonify(bulletin_data), 200
    else:
        return {'message': 'Ha ocurrido un error inesperado.'}, 500
    


@bulletins_bp.post('/pay/<path:id>')
@login_required
def pay_bulletin(id: str):
    """Pay a bulletin

    Keyword arguments:
    id -- the id given in the url

    POST arguments received (request.form):
    payment_method -- the payment method used to pay the bulletin (CASH OR CARD)
    price -- the price of the bulletin
    duration -- the duration of the bulletin
    """
    try:
        # Get the bulletin
        bulletin = BulletinModel.get_bulletin(id)

        # Check if the bulletin exists and if it has been paid
        if not bulletin:
            return jsonify({'message': "El boletin que se ha intentado pagar no existe"}), 400
        if bulletin.paid:
            return jsonify({'message': "El boletin ya ha sido indicado"}), 400
        
        # Get and check the payment method
        payment_method = request.form.get('payment_method')
        payment_method_used: PaymentMethod
        if not payment_method:
            payment_method_used = None
        else:
            payment_method_used = PaymentMethod.get_enum_value(payment_method)
        if not payment_method_used:
            return jsonify({'message': "El metodo de pago no ha sido indicado o no existe"}), 400
        
        # Get and check the price
        price = request.form.get('price')
        if not price:
            return jsonify({'message': "El precio no ha sido indicada o no existe"}), 400
        
        # Get and check the duration
        duration = request.form.get('duration')
        if not duration:
            return jsonify({'message': "La duración no ha sido indicada o no existe"}), 400


        # Pay the bulletin
        paid_bulletin = BulletinModel.pay_bulletin(id, payment_method_used, price, duration)
        if(paid_bulletin == None):
            return jsonify({'message': "El boletin no pudo ser pagado"}), 400
        

        # Add the withheld to the user if the payment method used to pay the ticket is cash
        if payment_method_used == PaymentMethod.CASH:
            add_withheld_to_user(paid_bulletin.responsible, paid_bulletin.price)
        
        
        return jsonify(paid_bulletin.to_json()), 200
    
    except Exception as exception:
        print(exception)
        return jsonify({'message': str(exception)}), 400
    




""" ------------------------ AVAILABLE BULLETINS ------------------------ """


@bulletins_bp.get('/available')
@login_required
def available_bulletins():
    available_bulletins = AvailableBulletinModel.get_available_bulletins()
    return jsonify(available_bulletins)




@bulletins_bp.get('/available-bulletins')
@login_required
def available_bulletins_page():
    available_bulletins = AvailableBulletinModel.get_available_bulletins()
    
    return render_template('available-bulletins.html', available_bulletins = available_bulletins);



@role_required("ADMIN")
@bulletins_bp.post('/available-bulletins/create')
def create_available_bulletin():
    # get request infor from post form
    request_info = request.form
    bulletin_duration = request_info.get('duration')
    bulletin_price = Decimal(request_info.get('price'))

    if bulletin_duration == None or bulletin_price == None:
        flash('No se ha podido crear un nuevo modelo de boletín.', 'error')
        return redirect(url_for('bulletins.available_bulletins_page')), 301
    
    
    try:
        bulletin = AvailableBulletinModel.create_available_bulletin(bulletin_duration, float(bulletin_price))
    except Exception as e:
        flash('No se ha podido crear un nuevo modelo de boletín.', 'error')
        return redirect(url_for('bulletins.available_bulletins_page')), 301
    
    if bulletin == None:
        flash('No se ha podido crear un nuevo modelo de boletín.', 'error')
        return redirect(url_for('bulletins.available_bulletins_page')), 301

    flash('El boletín ha sido creado con éxito', 'success')
    return redirect(url_for('bulletins.available_bulletins_page')), 301


@role_required("ADMIN")
@bulletins_bp.post('/available-bulletins/edit/<id>')
def edit_available_bulletin(id):
    """Edit an available bulletin and exeecute a flash message depending on the result
    
    Keyword arguments:
    id -- the id given in the url
    
    POST arguments received:
    duration -- the new duration of the bulletin (optional)
    price -- the new price of the bulletin (optional)
    Return: redirect to available bulletins page, 301
    """

    # Getting the request info
    available_bulletin_id = int(id)
    request_info = request.form
    available_bulletin = AvailableBulletinModel.get_available_bulletin(available_bulletin_id)


    bulletin_duration = request_info.get('duration', available_bulletin.duration)
    
    if bulletin_duration == '':
        bulletin_duration = available_bulletin.duration
    
    bulletin_price = request_info.get('price')
    if bulletin_price == None or request_info.get('price') == '':
        bulletin_price = available_bulletin.price
    else:
        bulletin_price = Decimal(bulletin_price)

    if bulletin_duration == None or bulletin_price == None:
        flash('Ha ocurrido un error editando el modelo de boletín.', 'error')
        return redirect(url_for('bulletinss.available_bulletinss_page')), 301

    edited_bulletin = AvailableBulletinModel.edit_available_bulletin(available_bulletin_id, bulletin_duration, bulletin_price);

    if edited_bulletin:
        flash('El modelo de boletín ha sido editado con éxito', 'success')
        return redirect(url_for('bulletins.available_bulletins_page')), 301
    else:
        flash('Ha ocurrido un error editando el modelo de boletín.', 'error')
        return redirect(url_for('bulletins.available_bulletins_page')), 301




@role_required("ADMIN")
@bulletins_bp.post('/available-bulletins/delete/<path:id>')
def delete_available_bulletin(id):
    available_bulletin_id = int(id)
    bulletin_deleted = AvailableBulletinModel.delete_available_bulletin(available_bulletin_id)

    if bulletin_deleted:
        flash('El modelo de boletín ha sido eliminado con éxito', 'success')
        return redirect(url_for('bulletins.available_bulletins_page')), 301
    else:
        flash('No se ha podido eliminar el modelo de boletín.', 'error')
        return redirect(url_for('bulletins.available_bulletins_page')), 301