from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Users model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Relationship to Cart
    cart = db.relationship('Cart', backref='user', lazy=True)

# Cart model (centralized for all items)
class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

# CartItem model (can store items from different categories)
class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_type = db.Column(db.String, nullable=False)  # Stores type of product (e.g., 'clothes', 'artwork')
    product_id = db.Column(db.Integer, nullable=False)  # ID of the product from the relevant table
    quantity = db.Column(db.Integer, default=1)

# Clothes model
class Clothes(db.Model):
    __tablename__ = 'clothes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)

# WhatsNew model
class WhatsNew(db.Model):
    __tablename__ = 'whats_new'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.Text)
    release_date = db.Column(db.Date)

# FlashSale model
class FlashSale(db.Model):
    __tablename__ = 'flash_sale'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

# HotInCategory model
class HotInCategory(db.Model):
    __tablename__ = 'hot_in_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('clothes.id'), nullable=False)

# Artwork model
class Artwork(db.Model):
    __tablename__ = 'artwork'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist_name = db.Column(db.String)
    image_url = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

# Shoes model
class Shoes(db.Model):
    __tablename__ = 'shoes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)

# Electronics model
class Electronics(db.Model):
    __tablename__ = 'electronics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)

# Books model
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)
