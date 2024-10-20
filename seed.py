from models import db, User, Product  # Removed Item
from app import app
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text  # Import for executing raw SQL

# Function to create users
def create_users():
    """Create and return admin and regular users."""
    admin_user = User(
        name="AdminUser", 
        email="admin@example.com", 
        role="admin"
    )
    admin_user.password = "adminpassword"  # Set password

    regular_user = User(
        name="RegularUser", 
        email="user@example.com", 
        role="user"
    )
    regular_user.password = "userpassword"  # Set password

    regular_user1 = User(
        name="RegularUser1", 
        email="user1@example.com", 
        role="user"
    )
    regular_user1.password = "userpassword1"  # Set password

    return admin_user, regular_user, regular_user1

# Function to create products
def create_products(admin_user):
    """Create products associated with the admin user."""
    products = [
        Product(
            name="Shoe Product", 
            description="A sample product for testing.", 
            price=1099, 
            item_availability=50, 
            user_id=admin_user.id  # Associate product with admin user
        ),
        Product(
            name="Clothes Product", 
            description="A high-quality premium product.", 
            price=2599, 
            item_availability=20, 
            user_id=admin_user.id
        ),
        Product(
            name="Books Product", 
            description="An affordable budget product.", 
            price=599, 
            item_availability=100, 
            user_id=admin_user.id
        )
    ]
    return products

# Function to seed data
def seed_data():
    """Seed the database with sample data."""
    try:
        # Create users
        admin_user, regular_user, regular_user1 = create_users()
        db.session.add(admin_user)
        db.session.add_all([regular_user, regular_user1])
        db.session.commit()

        # Create products associated with the admin user
        products = create_products(admin_user)
        db.session.add_all(products)
        db.session.commit()

        print("Database seeded successfully with Admin, Users, and Products!")

    except IntegrityError as ie:
        print(f"Integrity error occurred: {ie}")
        db.session.rollback()  # Roll back the transaction in case of integrity errors

    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
        db.session.rollback()  # Roll back in case of any other exceptions

# Main execution block
if __name__ == '__main__':
    with app.app_context():
        # Drop all tables, recreate them, and seed the database
        try:
            # Drop all tables using CASCADE to handle foreign key dependencies
            db.session.execute(text("DROP TABLE IF EXISTS items CASCADE"))
            db.session.execute(text("DROP TABLE IF EXISTS products CASCADE"))
            db.session.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            db.session.commit()

            # Recreate tables
            db.create_all()  
            seed_data()  # Seed the database

        except Exception as e:
            print(f"An error occurred while setting up the database: {e}")
            db.session.rollback()
