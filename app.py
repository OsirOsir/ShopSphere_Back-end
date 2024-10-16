from flask import Flask, jsonify, request, render_template, make_response, Blueprint
from models import db, User, Item, SpecialCategory, Cart, CartItem, Product
from flask_migrate import Migrate
from serializers import user_serializer, product_serializer, item_serializer
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shopsphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    """Decorator to ensure the current user is an admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Creates a blueprint for cart routes
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)

    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    cart_item = CartItem.query.filter_by(cart_id=cart.id, item_id=item.id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, item_id=item.id, quantity=quantity)
        db.session.add(cart_item)

    cart.update_total()
    db.session.commit()

    return jsonify({'message': 'Item added to cart'}), 201

@cart_bp.route('/cart/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({'message': 'Cart is empty'}), 404

    cart_items = [{
        'item': item.item.item_name,
        'quantity': item.quantity,
        'subtotal': item.subtotal
    } for item in cart.items]

    return jsonify({'items': cart_items, 'total': cart.total_price}), 200

@cart_bp.route('/cart/update', methods=['PUT'])
def update_cart():
    data = request.get_json()
    cart_item = CartItem.query.filter_by(cart_id=data['cart_id'], item_id=data['item_id']).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404

    cart_item.quantity = data['quantity']
    cart_item.cart.update_total()
    db.session.commit()

    return jsonify({'message': 'Cart updated'}), 200

@cart_bp.route('/cart/delete', methods=['DELETE'])
def delete_from_cart():
    data = request.get_json()
    cart_item = CartItem.query.filter_by(cart_id=data['cart_id'], item_id=data['item_id']).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404

    db.session.delete(cart_item)
    cart_item.cart.update_total()
    db.session.commit()

    return jsonify({'message': 'Item deleted from cart'}), 200

# Register the cart blueprint
app.register_blueprint(cart_bp)

@app.route('/')
def index():
    return "<h1>Welcome to ShopSphere</h1>"

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user_serializer(user) for user in users]), 200

    elif request.method == 'POST':
        data = request.json

        required_fields = ['name', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Name, email, and password are required'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this email already exists'}), 400

        try:
            role = data.get('role', 'user')
            new_user = User(
                name=data['name'], 
                email=data['email'], 
                role=role
            )
            new_user.password = data['password']
            db.session.add(new_user)
            db.session.commit()

            return jsonify(user_serializer(new_user)), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Database integrity error occurred'}), 500

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()

    if user and user.is_active and user.authenticate(data.get('password')):  
        login_user(user)
        return jsonify({'message': 'Login successful', 'user': user_serializer(user)}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

# User logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# User profile
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify(user_serializer(current_user)), 200

# Admin routes for managing products
@app.route('/admin/products', methods=['POST'])
@login_required
@admin_required
def add_product():
    data = request.json

    if 'name' not in data or 'price' not in data or 'user_id' not in data:
        return jsonify({'error': 'Name, price, and user_id are required'}), 400

    try:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            item_availability=data.get('item_availability', 0),
            user_id=data['user_id']
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify(product_serializer(new_product)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get user by ID
@app.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify(user_serializer(user)), 200
    return jsonify({'error': 'User not found'}), 404

# Admin delete user
@app.route('/users/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': f'User {id} deleted successfully.'}), 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'User not found'}), 404

# Additional category and item-related routes
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
        items = Item.query.filter(Item.is_flash_sale == True).all()
        return jsonify([item_serializer(item) for item in items])



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
    app.run(port=5555)
