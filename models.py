from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import MetaData

# Initialize SQLAlchemy and Bcrypt
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)  

    @hybrid_property
    def password(self):
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

# Cart model
class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)
    total_price = db.Column(db.Float, nullable=False, default=0.0)

    # Method to update the total price of the cart
    def update_total(self):
        self.total_price = sum([item.subtotal for item in self.items])

# CartItem model
class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item = db.relationship('Item')

    # Calculate the subtotal for the cart item
    @property
    def subtotal(self):
        return self.quantity * self.item.price

# Item model
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    items_available = db.Column(db.String, nullable=True)
    offer_price = db.Column(db.Integer)
    image_url = db.Column(db.Text, nullable=False)

    special_categories = db.relationship('SpecialCategory', secondary='item_special_categories', backref=db.backref('items', lazy=True))

# SpecialCategory model
class SpecialCategory(db.Model):
    __tablename__ = "special_categories"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

# Association table for Item and SpecialCategory
item_special_categories = db.Table('item_special_categories', 
                                   db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True), 
                                   db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True))
