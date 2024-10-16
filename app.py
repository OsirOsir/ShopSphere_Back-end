from flask import Flask, jsonify, request, make_response
from models import db, Item, SpecialCategory
from flask_migrate import Migrate
from serializers import item_serializer
from flask_restful import Resource, Api

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
    


if __name__ == '__main__':
    app.run(debug=True, port=5555)
