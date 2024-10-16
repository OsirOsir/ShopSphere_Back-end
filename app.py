from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Item  # Import db and Item from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shopsphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  

# Custom error handler for 404 errors (test)
@app.errorhandler(404)
def not_found(error):
    return "404 - Page Not Found", 404

# Route to fetch all items (test)
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()  
    return jsonify([{
        'id': item.id,
        'name': item.item_name,
        'description': item.description,
        'price': item.price,
        'image_url': item.image_url,
        'category': item.category,
        'items_available': item.items_available
    } for item in items])

# Route to purchase an item
@app.route('/items/<int:item_id>/purchase', methods=['POST'])
def purchase_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.items_available > 0:
        try:
            item.items_available -= 1
            db.session.commit()
            return jsonify({'message': 'Purchase successful!', 'item': item.item_name}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'Purchase failed due to an integrity error!'}), 500
    return jsonify({'message': 'Item is out of stock!'}), 400

# Route to notify users if an item is out of stock
@app.route('/items/<int:item_id>/notify', methods=['POST'])
def notify_users_if_out_of_stock(item_id):
    item = Item.query.get_or_404(item_id)
    if item.items_available <= 0:
        return jsonify({'message': f'Users notified about {item.item_name} being out of stock!'}), 200
    return jsonify({'message': 'Item is still in stock!'}), 200

if __name__ == '__main__':
    with app.app_context():  
        db.create_all() 
    app.run(debug=True)
