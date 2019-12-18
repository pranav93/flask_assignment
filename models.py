from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, UniqueConstraint

ma = Marshmallow()
db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    __table_args__ = (UniqueConstraint('name', name='_category_name_uc'),
                      )


class Gift(db.Model):
    __tablename__ = 'gifts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)


class EmployeeInterest(db.Model):
    __tablename__ = 'employee_interests'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), nullable=False)
    interest_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    __table_args__ = (UniqueConstraint('employee_id', 'interest_id', name='_employee_interest_uc'),
                      )
    
    
class GiftCategory(db.Model):
    __tablename__ = 'gift_categories'
    id = db.Column(db.Integer, primary_key=True)
    gift_id = db.Column(db.Integer, ForeignKey('gifts.id'), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    __table_args__ = (UniqueConstraint('gift_id', 'category_id', name='_gift_category_uc'),
                      )
