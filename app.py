from flask import Flask, jsonify, request, abort, make_response
from models import db, User, Item, SpecialCategory
from flask_migrate import Migrate
from serializers import user_serializer
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError # conditions are met
from serializers import item_serializer
from flask_restful import Resource, Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shopsphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)


def is_admin():
    # Check if the current user is an admin (pseudo-code for demonstration purposes)
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401, "Unauthorized: No token provided")
    
    token = auth_header.split(" ")[1]  # Assuming Bearer token is used
    user = User.query.filter_by(token=token).first()  # Replace with actual token validation
    if not user or not user.is_admin:
        abort(403, "Forbidden: Admins only")
    return user


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
        
        # Validate input
        if 'name' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400

        # Create a new user and set the password
        new_user = User(name=data['name'], email=data['email'])
        new_user.password = data['password']  # Use the password setter to hash the password

        # Add user to the session and commit
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_serializer(new_user)), 201

# Admin routes for items
@app.route("/api/items", methods=["POST"])
def create_item():
    is_admin()  # Check if the user is an admin
    data = request.json
    new_item = Item(
        item_name=data['item_name'],
        description=data.get('description'),
        price=data['price'],
        category=data['category'],
        image_url=data['image_url']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created successfully"}), 201


@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    is_admin()  # Check if the user is an admin
    item = Item.query.get_or_404(item_id)
    data = request.json
    item.item_name = data.get('item_name', item.item_name)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.category = data.get('category', item.category)
    item.image_url = data.get('image_url', item.image_url)
    db.session.commit()
    return jsonify({"message": "Item updated successfully"}), 200


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    is_admin()  # Check if the user is an admin
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

# Example routes for displaying items (no admin check required)
@app.route("/api/clothes", methods=["GET"])
def display_clothes():
    items = Item.query.filter_by(category="Clothes").all()
    return jsonify([item_serializer(item) for item in items])

@app.route("/api/shoes", methods=["GET"])
def display_shoes():
    items = Item.query.filter_by(category="Shoes").all()
    return jsonify([item_serializer(item) for item in items])

# Other routes omitted for brevity

if __name__ == '__main__':
    app.run(debug=True, port=5555)
