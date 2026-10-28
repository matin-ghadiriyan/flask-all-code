#barye sakhte virtaulenv az in dastor ra dar cmd mizanim ==> python -m virtualenv {nae virtualenv}
#baraye raftan bedakhelesh varede folderi ke vnv sakhte rafte va baad dakhele Scripts va activate ra mizanim
#va ba neveshtane ==>  deactivate az on sahe mitoni beyay biron
#baraye code haii ke marboot be python hast << {{ python -m }} >> yadet nare
#https://www.windsurf.com/profile?response_type=token&client_id=3GUryQ7ldAeKEuD2obYnppsnmj58eP5u&redirect_uri=vscode://Codeium.codeium&state=01d0ba72-f1f1-4e11-90e7-01f7ed62e323&scope=openid+profile+email&prompt=login&redirect_parameters_type=fragment 
#baraye sakhte filei kective hameye ketabkhane ha toosh bashe ma file requirement misazim ba in dastor ('cmd') ==> python -m pip freeze > requirements.txt
from flask import Flask  , Blueprint , render_template , jsonify , request , redirect , url_for , make_response , session , abort , flash , send_from_directory , current_app
from flask_wtf.csrf import CSRFProtect
import datetime
from time import time
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import mysql.connector
from sqlalchemy import case , select , desc
from sqlalchemy.ext.hybrid import hybrid_property
import config
#baraye code nevisi behtar ghesmate dovome code nevisi moratab ro bebin va route hari mibari toye ye file dige va daste bandishon mikoni baad dar file asli import miconi va mesle khate app.register_blueprint(blue1print) miyay regoster mikoni
#baraye db ham bayad on ra dakhele ye file moghaza taarif koni va baad be ingha import koni
mybd = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='website'
)
blue1print = Blueprint('blue1print' , __name__)
cursor = mybd.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS flask(name VARCHAR(255),age INT )')
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE
db = SQLAlchemy(app)
class User(db.Model , SerializerMixin):
    __tablename__="users"
    serialize_rules = ('-orders.user',)#vaghti mikhay az to_dict estefade koni bayad migheee relationship ha in khat ra ezafe koni ke error nade
    name = db.Column(db.String(50) , default='None')
    age = db.Column(db.Integer , nullable=False)
    id = db.Column(db.Integer ,autoincrement=True , primary_key=True)
    orders= db.relationship('Order' , back_populates='user')
    phon_user= db.relationship('Phon' , back_populates='user' , uselist=False)
    students = db.relationship('register' , back_populates='student')
    __table_args__=(
        db.UniqueConstraint('name' , 'age' , name="UI_A_N"),
        db.CheckConstraint("name =! 'hooshang'" , name="Check"),
        db.Index('IN_A_N' , 'age' , 'name'),
    )
    @hybrid_property
    def count_order_user(self):
        return len(self.orders)
    @count_order_user.expression
    def count_order_user(cls):
        return select(db.func.count(Order.id)).where(Order.id == cls.id)
class Order(db.Model , SerializerMixin):
    __tablename__="orders"
    users_id_name = db.Column(db.String(50) , default='None')
    users_id_age = db.Column(db.Integer , nullable=False)
    id = db.Column(db.Integer ,autoincrement=True)
    user = db.relationship('User' , back_populates='orders')
    __table_args__=(
        db.PrimaryKeyConstraint('id' , name="PK_Id"),
        db.ForeignKeyConstraint(['users_id_name'],['users.name'],onupdate="CASCADE",ondelete="RESTRICT")
    )
class Phon(db.Model):
    __tablename__="users_phon"
    adress = db.Column(db.String(500))
    phon = db.Column(db.Integer , nullable=False)
    id = db.Column(db.Integer ,autoincrement=True)
    name = db.Column(db.String(50) , nullable=False)
    user = db.relationship('User', back_populates='phon_user')
    __table_args__=(
        db.PrimaryKeyConstraint('id' , name="PK_Id"),
        db.ForeignKeyConstraint(['id'],['users.id'],onupdate="CASCADE",ondelete="RESTRICT")
    )
class register(db.Model , SerializerMixin):
    __tablename__="registers"
    teacher_id = db.Column(db.Integer)
    User_id = db.Column(db.Integer)
    id = db.Column(db.Integer ,autoincrement=True)
    student = db.relationship('User' , back_populates='students')
    teacher = db.relationship('Teacher' , back_populates='teachers')
    __table_args__=(
        db.PrimaryKeyConstraint('id' , name="PK_Id"),
        db.ForeignKeyConstraint(['User_id'],['users.id'],onupdate="CASCADE",ondelete="RESTRICT"),
        db.ForeignKeyConstraint(['teacher_id'],['teachers.id'],onupdate="CASCADE",ondelete="RESTRICT")
    )
class Teacher(db.Model , SerializerMixin):
    __tablename__="teachers"
    id = db.Column(db.Integer ,autoincrement=True)
    name = db.Column(db.String(50) , nullable=False)
    teachers = db.relationship('register' , back_populates='teacher')
    __table_args__=(
        db.PrimaryKeyConstraint('id' , name="PK_Id"),
    )
class Login(db.Model , SerializerMixin):
    __tablename__="logins"
    id = db.Column(db.Integer ,autoincrement=True)
    name = db.Column(db.String(50) , nullable=False)
    age = db.Column(db.Integer , nullable=False)
    __table_args__=(
        db.PrimaryKeyConstraint('id' , name="PK_Id"),
        db.UniqueConstraint('name' , 'age' , name="UI_A_N"),
    )
with app.app_context():
    db.create_all()
@blue1print.route("/")
def home():
    name = "new user"
    return "<a href='about'>about</a>"
@blue1print.route("/about")
def about():
    return "<b><h1>this is a about</h1></b>"
@blue1print.route("/age/<int:age>")
def age_get(age):
    return f"your age is:{age}"
@app.route("/form/<int:age2>/<name>")
def name_get(name , age2):
    return f"name:{name}:{age2}"
@app.route('/main/<name>')
def main_page(name):
    if name == 'matin' or name == 'mohammad matin':
        return render_template('html_flask_file.html' , name=name)#baraye import kardane ye file dar barname bayad in ghori benevisi vali bayad esme folderi ke kenare filet hatman bayad bashe (ke tosh file html hast) bayad esmesh templates bashe
    else:
        return f"your name is not right (({name}))"
@app.route('/register' , methods=["POST"])
def register_function():
    password_user = request.form['passwordf']
    age_user  = request.form['fage']
    name_user = request.form['fname']
    return f'<p>your password: {password_user}</p><br><p>your name: {name_user}</p><br><p>your age: {age_user}</p>'
@app.route('/register_get' , methods=["GET" , 'POST'])
def register_get():
    if request.method == "GET":
        password_user = request.args.get('passwordf')#ersal ba methode get
        age_user  = request.args.get('fage')
        name_user = request.args.get('fname')
    elif request.method == "POST":
        password_user = request.form['passwordf']#ersal ba methode post
        age_user  = request.form['fage']
        name_user = request.form['fname']
    return f'<p>your password: {password_user}</p><br><p>your name: {name_user}</p><br><p>your age: {age_user}</p>'
@app.route('/aboutus/<user_name>')
def aboutus(user_name):
    return redirect(f'/main/{user_name}',301)#baraye vaghti hast ke miukhay besorate movaghat behesh vasl beshe va gar daeem bood 302 bezan
@app.route('/aboutus2')
def aboutus2():
    return redirect(url_for('about'),301)
@app.route('/cookie/<name>')
def cookie(name):
    resp = make_response(render_template('html_flask_file.html'))#sakhte cookie
    resp.set_cookie('name_cookie',name,max_age=1*60)
    #baraye hazf kardane cookie ===>   resp.set_cookie("name" , "" , expire=0)
    return resp
@app.route('/cookie_name')
def cookie_name():
    if "name_cookie" in request.cookies:
        name = request.cookies['name_cookie']
    else:
        name = 'new user'
    return render_template('html_flask_file.html' , name=name) 
@app.route('/main/register2' , methods=["POST"])
def register2():
    select = request.form['select']
    redio = request.form['.radio.']
    fileload = request.sk['fileload']
    fileload.save('Upload/'+str(time())+'.'+fileload.filename.split('.')[1])
    return render_template(f'your select id:{select} your radio is:{redio}')
@app.route('/login' , methods=['POST' , 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(days=3)
        name = request.form['name']
        if name == 'matin':
            session['name'] = name
            return redirect('dashbord')
        else:
            return redirect(url_for('login'))
@app.route('/dashbord')
def dashbord():
    if session.get('name'):
        return 'your name is '+session.get('name')+' '+'<a href="logout">logout</a>'
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('name' , None)
    return redirect(url_for('dashbord'))
@app.route('/abort/<int:code_error>')
def abort_error(code_error):
    abort(code_error)
@csrf.exempt
@app.route('/flash' , methods=['POST','GET'])
def flash_error():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        session.permanent = True
        import datetime
        app.permanent_session_lifetime = datetime.timedelta(days=3)
        name = request.form['name']
        if name == 'matin':
            session['name'] = 'matin'
            return redirect('dashbord')
        else:
            flash("your name is not write" , 'error')
            flash("your name is error 2" , 'info')
            return redirect(url_for('flash_error'))
@app.route('/file')
def file_downlowd():
    #ingha adrese file ra midi va baad be directory midish va esme file ra be path dar send_file_firectory midi
    #baraye download kardan as_attachment=True ra mizanim vali agar nazanim faghat mohtavaye file ra neshan mide
    adress_file = os.path.join(current_app.root_path , 'download_file/' )
    return send_from_directory(directory=adress_file , path='nesh.png',as_attachment=False)
@app.route('/mysql_form' , methods=['POST'])
def mysql_form():
    cursor = mybd.cursor()
    name = request.form['user_name']
    age = request.form['user_age']
    age_list = []
    name_list = []
    cursor.execute("SELECT * FROM  flask")
    result = cursor.fetchall()
    for list in result:
        name_list.append(list[0])
        age_list.append(list[1])
    cursor.execute("")
    cursor.execute("INSERT INTO flask (`name` , `age`) VALUE (%s,%s)" , [name , age])
    mybd.commit()
    return f'name is: {name} and age is: {age}<br><br><br>{name_list}<br><br><br>{age_list}'
@app.route('/mysql_ORM' , methods=['POST'])
def mysql_ORM():
    name_id = request.form['user_name']
    age_id = request.form['user_age']
    user = User(name=name_id , age=age_id)
    db.session.add(user)
    db.session.commit()
    return f'name is: {name_id} and age is: {age_id}'
@app.route('/add-order' , methods=['POST'])
def add_order():
    name = request.form['user_name']
    age = request.form['user_age']
    user = User.query.filter(User.name == name).first_or_404()
    order = Order(users_id_name=name , users_id_age=age , id="NULL")
    user.orders.append(order)
    db.session.add(order)
    db.session.commit()
    return 'down'
@app.route('/add-phon' , methods=['POST'])
def add_phon():
    name = request.form['user_name']
    phon_number = request.form['user_age']
    adress = request.form['adress']
    users = User.query.filter(User.name == name).first_or_404()
    phon = Phon(name=name , adress=adress , phon=phon_number)
    users.phon_user = phon
    db.session.add(phon)
    db.session.commit()
    return 'down'
@app.route('/login-ORM' , methods=['POST'])
def login_ORM():
    name = request.form['name']
    age = request.form['age']
    login = Login(name=name , age=age)
    db.session.add(login)
    db.session.commit()
    return f'name is: {name} and age is: {age} <br> <a href="/get-mysql">get your mysql save</a>'
@app.route('/get-mysql')
def get_mysql():
    login = Login.query.all()
    login_name = Login.query.with_entities(Login.name , Login.id.label('id_login') , db.func.count(User.name)).filter(User.name == 'matin').order_by(User.id.desc()).having(db.func.count(User.name) > 1).limit(3).all()
    #baraye didane filter haye bishtar ghesmate 34 ra bebin
    age_avg = Login.query.with_entities(db.func.avg(Login.age),User.name).order_by(Login.name).first()#you can write (first_or_404()) or (all()) or (first())
    return render_template('html_flask_file.html' , login=login , name = login_name , age_avg=age_avg)
@app.route('/login_ORM_Updata' , methods=['POST'])
def login_ORM_Updata():
    name = request.form['name']
    age = request.form['age']
    name_in_sql = request.form['name_in_sql']
    login = Login.query.filter(Login.name == name_in_sql).first_or_404()
    login.name = name
    login.age = age
    db.session.commit()
    return f'name is: {name} and age is: {age} <br>'
@app.route('/login-ORM-Delete' , methods=['POST'])
def login_ORM_Delete():
    name = request.form['name']
    login = Login.query.filter(Login.name == name).first_or_404()
    db.session.delete(login)
    db.session.commit()
    return f'name is: {name}<br>'
@app.route('/get-mysql-html')
def get_html():
    case_mysql = case(
            (Login.age < 18, "child"),
            (Login.age > 18, "Up"),
            else_='your age is 18'
    )
    user1 = User.query.with_entities(User.name)
    user2 = Order.query.with_entities(Order.users_id_age)
    users = user1.union(user2)
    login = Login.query.with_entities(case_mysql.label('case') , Login.name , Login.age).order_by(Login.age).all()
    #mitoni beghaye order_by az group_by ham estefade koni ke order_by baraye label hast ke label ra midi vali group_by baraye name soton hast
    return render_template('html_flask_file.html', union = users, login=login , user=User.query.with_entities(Order.users_id_name.label('name') , Order.users_id_age.label('age') , User.id).join(Order , User.name == Order.users_id_name).first() , login_2 = User.query.all())
# app.register_blueprint(blue1print)
@csrf.exempt
@app.route('/API' , methods=['post'])
def API():
    json_apikey = request.json['apikey'] if request.json != None else None
    if json_apikey != '1234567890':
        return jsonify({'Error.Json.API.Key':'error'})
    Users = User.query.all()
    dectionery_Users = [user.to_dict(only=('name' , 'age' , 'id' , 'orders')) for user in Users]
    return jsonify({'Error.Json.API.Key':'ok' , 'data':dectionery_Users})
@app.route('/database')
def database():
    user = User.query.order_by(desc(User.count_order_user)).all()
    return render_template('html_flask_file.html' , user=user)
if __name__ == '__main__':
    app.run(debug=config.DEBUG_APP_FLASK,port=config.PROT_APP_FLASK)