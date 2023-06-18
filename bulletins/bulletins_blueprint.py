from flask import Blueprint, request, jsonify
from auth.controllers.login import login_required

from .models.bulletin_model import BulletinModel
from .entities.bulletin import Bulletin
import datetime


bulletins_bp = Blueprint('bulletins', __name__, url_prefix='/bulletins')



@bulletins_bp.get('/get-bulletin/<id>')
@login_required
def get_bulletin(id: int):
    bulletin = BulletinModel.get_bulletin(id)
    if bulletin != None:
        return jsonify(bulletin.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo el boletín indicado'}, 500


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
            bulletin_json["paid"], 
            bulletin_json["brand"], 
            bulletin_json["model"], 
            bulletin_json["signature"], 
            bulletin_json['created_at'])
        
        
    except Exception as e:
        return {'message': 'El boletín no pudo ser creado.'}, 400


    if bulletin != None:
        bulletin_data: dict = bulletin.to_json()
        return jsonify(bulletin_data), 200
    else:
        return {'message': 'El boletín no pudo ser creado.'}, 500




