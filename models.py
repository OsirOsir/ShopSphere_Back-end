from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
# db = SQLAlchemy()
    
    
item_special_categories = db.Table('item_special_categories', 
                                   db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True), 
                                   db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True))
    
# Item 
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
    
    special_categories = db.relationship('SpecialCategory', secondary=item_special_categories, backref=db.backref('items', lazy=True))
    
class SpecialCategory(db.Model):
    __tablename__ = "special_categories"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


