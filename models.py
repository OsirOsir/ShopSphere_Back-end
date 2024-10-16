from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from sqlalchemy import MetaData

# Initialize SQLAlchemy and Bcrypt
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()

# User model
class User(db.Model, UserMixin):
    """Represents a user in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)  

    # Relationship to the Product model
    products = db.relationship('Product', backref='owner', lazy=True)

    @hybrid_property
    def password(self):
        """Password is not readable."""
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, password):
        """Hash the password and store it."""
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.check_password_hash(self._password_hash, password)

    def is_admin(self):
        """Check if the user has admin privileges."""
        return self.role == 'admin'

    def get_id(self):
        """Return the user ID as a string."""
        return str(self.id)

    def __repr__(self):
        return f'<User(name={self.name}, email={self.email}, role={self.role}, is_active={self.is_active})>'

# Product model
class Product(db.Model):
    """Represents a product in the system."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    item_availability = db.Column(db.Integer, nullable=False, default=0)
    
    # Foreign key to associate with a User (owner)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Product(name={self.name}, price=${self.price}, item_availability={self.item_availability})>'

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

# Association table for many-to-many relationship between Item and SpecialCategory
item_special_categories = db.Table(
    'item_special_categories',
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
    db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True)
)

# Item Model
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    items_available = db.Column(db.Integer, nullable=False)
    offer_price = db.Column(db.Integer)
    image_url = db.Column(db.Text, nullable=False)

    # Many-to-many relationship with SpecialCategory
    special_categories = db.relationship(
        'SpecialCategory',
        secondary=item_special_categories,
        backref=db.backref('items', lazy=True)
    )

    # Check if the item is in stock
    def is_in_stock(self):
        return self.items_available > 0

# SpecialCategory Model
class SpecialCategory(db.Model):
    __tablename__ = "special_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

# Notification Model
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    # Relationship with Item
    item = db.relationship('Item', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification {self.message}>'
