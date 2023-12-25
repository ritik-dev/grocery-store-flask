from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from GroceryStore import login_manager,db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

purchases = db.Table('purchases',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('purchase_date', db.DateTime, nullable=False, default=datetime.utcnow)
)

class Orders(db.Model):
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_of_item = Column(Float, nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Define relationships with other tables
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = relationship('Orders', back_populates='user')
    purchases = db.relationship('Product', secondary=purchases, backref='buyers', lazy='dynamic')

    def is_active(self):
        return True

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Category('{self.name}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.DateTime, nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=True)
    rate_per_unit = db.Column(db.Float, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    orders = relationship('Orders', back_populates='product')
    image_file = db.Column(db.String(50), nullable=True, default='default.png')

    def __repr__(self):
        return f"Product('{self.name}', '{self.manufacture_date}', '{self.expiry_date}', '{self.rate_per_unit}')"
