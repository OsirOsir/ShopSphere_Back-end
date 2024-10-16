from models import db, User, Product
from app import app 
from sqlalchemy.exc import IntegrityError  # Import IntegrityError

def create_users():
    """Create and return admin and regular users."""
    admin_user = User(
        name="AdminUser", 
        email="admin@example.com", 
        role="admin"
    )
    admin_user.password = "adminpassword"  

    regular_user = User(
        name="RegularUser", 
        email="user@example.com", 
        role="user"
    )
    regular_user.password = "userpassword"  

    return admin_user, regular_user

def create_products(admin_user):
    """Create products associated with the admin user."""
    products = [
        Product(name="Shoe Product", description="A sample product for testing.", price=1099, item_availability=50, user_id=admin_user.id),
        Product(name="Clothes Product", description="A high-quality premium product.", price=2599, item_availability=20, user_id=admin_user.id),
        Product(name="Books Product", description="An affordable budget product.", price=599, item_availability=100, user_id=admin_user.id)
    ]
    return products

def seed_data():
    try:
        
        admin_user, regular_user = create_users()

        
        db.session.add(admin_user)
        db.session.add(regular_user)

        
        db.session.commit()

        
        products = create_products(admin_user)

        
        db.session.add_all(products)

        
        db.session.commit() 
        
        print("Database seeded successfully with Admin, User, and Products!")

    except IntegrityError as ie:
        print(f"Integrity error occurred: {ie}")
        db.session.rollback()  
    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
        db.session.rollback()  

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  
        db.create_all()  
        seed_data()
