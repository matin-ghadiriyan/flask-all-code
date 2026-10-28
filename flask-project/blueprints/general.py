from flask import Blueprint
import time, datetime,os
from flask import render_template,current_app,send_from_directory,flash,abort,request,redirect,session,url_for,make_response
from sqlalchemy import func,case,desc
from models.models import *
from extentions import db

general_blueprint = Blueprint("general_blueprint", __name__)

@general_blueprint.route("/", methods=["GET","POST"])
def home():
    if(request.method == "GET"):
        users = User.query.order_by(desc(User.total_orders_count)).all()

        if 'name' in request.cookies:
            name = request.cookies['name']
        else:
            name = "new user"
        return render_template("home/home.html",name = name, users=users)

    elif request.method == "POST" :
        name = request.form['fname']
        age = request.form['age']
        file1 = request.files['file1']
        file1.save('upload/'+str(time.time())+'.'+file1.filename.split(".")[1])

        return name + " " + age


@general_blueprint.route("/add-order", methods=["POST"])
def add_order():
    name = request.form["name"]
    email = request.form["email"]

    user = User.query.filter(User.email == email).first_or_404()
    order = Order(name = name)
    user.orders.append(order)

    db.session.add(order)
    db.session.commit()

    return "done"