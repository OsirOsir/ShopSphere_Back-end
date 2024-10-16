from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
    
    
item_special_categories = db.Table('item_special_categories', 
                                   db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True), 
                                   db.Column('special_category_id', db.Integer, db.ForeignKey('special_categories.id'), primary_key=True))
    
# Item Model

db = SQLAlchemy()

# Item Model
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    items_available = db.Column(db.Integer, nullable=False)  
    image_url = db.Column(db.Text, nullable=False)
    
    special_categories = db.relationship('SpecialCategory', secondary=item_special_categories, backref=db.backref('items', lazy=True))

#Special Category Model
class SpecialCategory(db.Model):
    __tablename__ = "special_categories"
    

    # Check if the item is in stock
    def is_in_stock(self):
        return self.items_available > 0  


# Notification Model
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    item = db.relationship('Item', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification {self.message}>'
