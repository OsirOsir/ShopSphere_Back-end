from flask_sqlalchemy import SQLAlchemy

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
