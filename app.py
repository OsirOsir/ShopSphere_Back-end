from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Item  # Import db and Item from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shopsphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)


@app.route("/api/clothes", methods=["GET"])
def display_clothes():
    clothes = Item.query.filter(Item.category == "Clothes").all()
    
    if not clothes:
        return jsonify({"message": "No clothes available currently."}), 404
    
    return jsonify([item_serializer(clothes_item) for clothes_item in clothes]), 200


@app.route("/api/shoes", methods=["GET"])
def display_shoes():
    shoes = Item.query.filter(Item.category == "Shoes").all()
    
    if not shoes:
        return jsonify({"message": "No shoes available currently."}), 404
    
    return jsonify([item_serializer(shoes_item) for shoes_item in shoes]), 200


@app.route("/api/artwork", methods=["GET"])
def display_artwork():
    artworks = Item.query.filter(Item.category == "Artwork").all()
    
    if not artworks:
        return jsonify({"message": "No artworks available currently."}), 404

    return jsonify([item_serializer(artworks_item) for artworks_item in artworks]), 200


@app.route("/api/electronics", methods=["GET"])
def display_electronics():
    electronics = Item.query.filter(Item.category == "Electronics").all()
    
    if not electronics:
        return jsonify({"message": "No electronics available currently."}), 404
    
    return jsonify([item_serializer(electronics_item) for electronics_item in electronics]), 200



@app.route("/api/books", methods=["GET"])
def display_books():
    books = Item.query.filter(Item.category == "Books").all()
    
    if not books:
        return jsonify({"message": "No books available currently."}), 404
    
    return jsonify([item_serializer(books_item) for books_item in books]), 200


class FlashSale(Resource):
    def get(self):
        items = Item.query.join(Item.special_categories).filter(SpecialCategory.name == "flash_sale").all()
        
        if items:
            return jsonify([item_serializer(item) for item in items])
        
        return jsonify({"message": "No items in Flash Sale section."})


class HotInCategory(Resource):
    def get(self):
        items = Item.query.join(Item.special_categories).filter(SpecialCategory.name == "hot_in_category").all()
        
        if items:  
            return jsonify([item_serializer(item) for item in items])
        
        return jsonify({"message": "No items in Hot In Category section."})
    

class WhatsNew(Resource):
    def get(self):
        items = Item.query.join(Item.special_categories).filter(SpecialCategory.name == "whats_new").all()
        
        if items: 
            return jsonify([item_serializer(item) for item in items])
        
        return jsonify({"message": "No items in What's New section."})
    
    
api.add_resource(FlashSale, '/api/flashsale', endpoint="flashSale")
api.add_resource(HotInCategory, '/api/hot_in_category', endpoint="hotInCategory")
api.add_resource(WhatsNew, '/api/whats_new', endpoint="whatsNew")
    
    
@app.route("/api/item/<int:item_id>/add_special_category", methods=["POST"])
def add_special_category_to_item(item_id):
    data = request.json
    special_category_name = data["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

    if special_category and item:
        item.special_categories.append(special_category)
        db.session.commit()
        return jsonify({"message": f"Special Category {special_category_name} added to item"}), 200
    
    return jsonify({"message": "Error: Item or Special Category not found"}), 404


@app.route("/api/item/<int:item_id>/remove_special_category", methods=["POST"])
def remove_special_category_from_item(item_id):
    data = request.json
    special_category_name = data["special_category_name"]
    
    item = Item.query.get(item_id)
    special_category = SpecialCategory.query.filter_by(name=special_category_name).first()

    if special_category and item:
        item.special_categories.remove(special_category)
        db.session.commit()
        return jsonify({"message": f"Special Category {special_category_name} removed from item"}), 200
    
    return jsonify({"message": "Error: Item or Special Category not found"}), 404


@app.route('/api/search_items', methods=["GET"])
def search_items():
    
    search_term = request.args.get('q', '')
    
    items = Item.query.filter(Item.item_name.ilike(f'%{search_term}%')).all()
    
    if items:
        return jsonify([item_serializer(item) for item in items]), 200
    
    return jsonify({"message": "No search results found."}), 404
    

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
