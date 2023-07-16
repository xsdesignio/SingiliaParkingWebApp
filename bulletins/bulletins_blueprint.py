from flask import Blueprint, render_template, request, jsonify
from auth.controllers.login import login_required

from .models.bulletin_model import BulletinModel
from .entities.bulletin import Bulletin



bulletins_bp = Blueprint('bulletins', __name__, url_prefix='/bulletins', template_folder='./templates')



@bulletins_bp.get('/')
@login_required
def bulletins_page():

    bulletins = BulletinModel.get_bulletins()

    return render_template('bulletins.html', bulletins=bulletins)



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
    try:
        bulletin = BulletinModel.create_bulletin(
            bulletin_json['responsible_id'], 
            bulletin_json["location"], 
            bulletin_json['registration'], 
            bulletin_json['duration'], 
            bulletin_json['price'],  
            bulletin_json['paid'],  
            bulletin_json['created_at'],
            bulletin_json.get("brand"), 
            bulletin_json.get("model"), 
            bulletin_json.get("color"),)
        
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


