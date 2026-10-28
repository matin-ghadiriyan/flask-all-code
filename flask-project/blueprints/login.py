from flask import Blueprint
import time, datetime,os
from flask import render_template,current_app,send_from_directory,request,redirect,session,url_for,make_response
from sqlalchemy import func,case
from models.models import *
from extentions import db

login_blueprint = Blueprint("login_blueprint", __name__)

@login_blueprint.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]

    user = User(name = name, email= email)
    db.session.add(user)
    db.session.commit()

    return "ثبت نام با موفقیت انجام شد"