from flask import Blueprint, jsonify,request
from models.models import User
from extentions import csrf

api_blueprint = Blueprint("api_blueprint", __name__)
csrf.exempt(api_blueprint)

@api_blueprint.route('/get_users', methods = ["POST"])
def get_users():
    apikey = request.json['apikey'] if request.json != None else None
    
    if apikey != 'jshdausidaysidgasyidas':
        return jsonify({'status':'error'})

    users = User.query.all()
    final_list = [user.to_dict(only=('name','email')) for user in users]
    return jsonify({'status':'ok', 'data':final_list})