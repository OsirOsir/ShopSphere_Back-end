from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

# User model
class User(db.Model, UserMixin):
    """Represents a user in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)  

    # Relationship to the Product model
    products = db.relationship('Product', backref='owner', lazy=True)

    @hybrid_property
    def password(self):
        """Password is not readable."""
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, password):
        """Hash the password and store it."""
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.check_password_hash(self._password_hash, password)

    def is_admin(self):
        """Check if the user has admin privileges."""
        return self.role == 'admin'

    def get_id(self):
        """Return the user ID as a string."""
        return str(self.id)

    def __repr__(self):
        return f'<User(name={self.name}, email={self.email}, role={self.role}, is_active={self.is_active})>'


# Product model
class Product(db.Model):
    """Represents a product in the system."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    item_availability = db.Column(db.Integer, nullable=False, default=0)
    
    # Foreign key to associate with a User (owner)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Product(name={self.name}, price=${self.price}, item_availability={self.item_availability})>'
