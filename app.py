from flask import Flask, jsonify, request
from models import db, User
from flask_migrate import Migrate
from serializers import user_serializer
from flask_bcrypt import Bcrypt  # is used to integrate password hashing and checking in a Flask application, providing a secure way to handle user authentication.
from sqlalchemy.exc import IntegrityError # conditions are met

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shopsphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

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

# Get user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return jsonify(user_serializer(user)), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Delete user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {id} deleted successfully.'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5555)

