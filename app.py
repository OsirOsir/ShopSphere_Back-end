from flask import Flask, jsonify, request
from models import db, User, Item, SpecialCategory
from flask_migrate import Migrate
from serializers import (user_serializer, item_serializer)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shopsphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "<h1>Welcome to ShopSphere</h1>"

# Users routes
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user_serializer(user) for user in users])
    
    elif request.method == 'POST':
        data = request.json
        new_user = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_serializer(new_user)), 201

@app.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def handle_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify(user_serializer(user))
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with id {user_id} has been deleted"}
    
    
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


# # Clothes routes
# @app.route('/clothes', methods=['GET'])
# def handle_clothes():
#     clothes = Clothes.query.all()
#     return jsonify([clothes_serializer(cloth) for cloth in clothes])

# # Whats New routes
# @app.route('/whats_new', methods=['GET'])
# def handle_whats_new():
#     whats_new_items = WhatsNew.query.all()
#     return jsonify([whatsnew_serializer(item) for item in whats_new_items])

# # Flash Sale routes
# @app.route('/flash_sale', methods=['GET'])
# def handle_flash_sale():
#     flash_sales = FlashSale.query.all()
#     return jsonify([flashsale_serializer(sale) for sale in flash_sales])

# # Hot In Category routes
# @app.route('/hot_in_category', methods=['GET'])
# def handle_hot_in_category():
#     hot_items = HotInCategory.query.all()
#     return jsonify([hotincategory_serializer(item) for item in hot_items])

# # Artwork routes
# @app.route('/artwork', methods=['GET'])
# def handle_artwork():
#     artworks = Artwork.query.all()
#     return jsonify([artwork_serializer(art) for art in artworks])

# # Shoes routes
# @app.route('/shoes', methods=['GET'])
# def handle_shoes():
#     shoes_list = Shoes.query.all()
#     return jsonify([shoes_serializer(shoe) for shoe in shoes_list])

# # Electronics routes
# @app.route('/electronics', methods=['GET'])
# def handle_electronics():
#     electronics_list = Electronics.query.all()
#     return jsonify([electronics_serializer(electronic) for electronic in electronics_list])

# # Books routes
# @app.route('/books', methods=['GET'])
# def handle_books():
#     books = Book.query.all()
#     return jsonify([book_serializer(book) for book in books])

# # Cart routes
# @app.route('/cart', methods=['GET'])
# def handle_cart():
#     carts = Cart.query.all()
#     return jsonify([cart_serializer(cart) for cart in carts])

# # Cart Item routes
# @app.route('/cart_item', methods=['GET'])
# def handle_cart_items():
#     cart_items = CartItem.query.all()
#     return jsonify([cartitem_serializer(item) for item in cart_items])

if __name__ == '__main__':
    app.run(debug=True, port=5555)
