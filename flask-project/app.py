from extentions import db,csrf
from config import *
from flask import Flask
from flask_migrate import Migrate
from blueprints.general import general_blueprint
from blueprints.login import login_blueprint
from blueprints.api import api_blueprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_CONFIG
app.secret_key = SECRET_KEY

db.init_app(app)
Migrate(app, db)
csrf.init_app(app)

app.register_blueprint(login_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True, port=PORT)