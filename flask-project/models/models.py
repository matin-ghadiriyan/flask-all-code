from extentions import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import func,select
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model,SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement = True)
    name = db.Column(db.String(50), default = "no name")
    email = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(11), nullable = True)
    orders = db.relationship("Order", back_populates="user")
    contact = db.relationship("Contact", back_populates="user", uselist=False)
    teacher = db.relationship("Registration", back_populates="user")

    __table_args__= (
        db.PrimaryKeyConstraint("id",name = "pk_id"),
        db.UniqueConstraint("name","email", name = "unique1"),
        db.CheckConstraint("name != 'hooshang'", name ="check_name"),
        db.Index('index1','name','email')
    )

    @hybrid_property
    def total_orders_count(self):
        return len(self.orders)

    @total_orders_count.expression
    def total_orders_count(cls):
        return (select([func.count(Order.id)]).where(Order.user_id == cls.id))

class Registration(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.Integer, autoincrement = True)
    user_id = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer)
    user = db.relationship("User", back_populates="teacher")
    teacher = db.relationship("Teacher", back_populates="user")

    __table_args__= (
        db.PrimaryKeyConstraint("id",name = "pk_id"),
        db.ForeignKeyConstraint(['user_id'],['users.id'], onupdate="CASCADE", ondelete="CASCADE"),
        db.ForeignKeyConstraint(['teacher_id'],['teachers.id'], onupdate="CASCADE", ondelete="CASCADE")
    )

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, autoincrement = True)
    name = db.Column(db.String(50), default = "no name")
    user = db.relationship("Registration", back_populates="teacher")

    __table_args__= (
        db.PrimaryKeyConstraint("id",name = "pk_id"),
    )

class Contact(db.Model):
    __tablename__ = "user_contact"
    id = db.Column(db.Integer, autoincrement = True)
    user_id = db.Column(db.Integer)
    address = db.Column(db.String(500))
    phone = db.Column(db.String(50))
    user = db.relationship("User", back_populates="contact")

    __table_args__= (
        db.PrimaryKeyConstraint("id",name = "pk_id"),
        db.ForeignKeyConstraint(['user_id'],['users.id'], onupdate="CASCADE", ondelete="CASCADE")
    )

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, autoincrement = True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    user = db.relationship("User", back_populates="orders")

    __table_args__= (
        db.PrimaryKeyConstraint("id",name = "pk_id"),
        db.ForeignKeyConstraint(['user_id'],['users.id'], onupdate="CASCADE", ondelete="CASCADE")
    )