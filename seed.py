from models import db, User, Product, Item, SpecialCategory
from app import app  
from sqlalchemy.exc import IntegrityError  # Import IntegrityError
from datetime import datetime
from faker import Faker
from sqlalchemy import text

# Code from authentication branch
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

# Code from main branch
db.session.execute(text("DELETE FROM item_special_categories"))

# Remove all rows from the tables
Item.query.delete()
SpecialCategory.query.delete()

# Reset primary key sequences to start at 1
db.session.execute(text("ALTER SEQUENCE items_id_seq RESTART WITH 1;"))
db.session.execute(text("ALTER SEQUENCE special_categories_id_seq RESTART WITH 1;"))

# Define your seed items
items = [ 
    Item(item_name="Casual T-Shirt", description="A comfortable and casual t-shirt for everyday wear.", price=1999, category="Clothes", items_available=50, image_url="Assets/clothes/black tshirt.jpeg"),
    # Additional items...
]

db.session.add_all(items)
print("Items seeded successfully!")

print("Seeding special categories...")

special_categories = [
    SpecialCategory(name="flash_sale"),
    SpecialCategory(name="hot_in_category"),
    SpecialCategory(name="whats_new")
]

db.session.add_all(special_categories)
db.session.commit()
print("Special categories seeded successfully!")

print("Adding items to special categories...")

flash_sale_special_category = SpecialCategory.query.filter_by(name="flash_sale").first()
hot_in_category_special_category = SpecialCategory.query.filter_by(name="hot_in_category").first()
whats_new_special_category = SpecialCategory.query.filter_by(name="whats_new").first()

flash_sale_items = [
    Item.query.filter(Item.item_name == "Classic Fit Polo Shirt").first(),
    # Additional items...
]

for item in flash_sale_items:
    if item and flash_sale_special_category not in item.special_categories:
        flash_sale_special_category.items.append(item)

# Similar loops for hot_in_category_items and whats_new_items...

db.session.commit()
print("Database seeded successfully!")

# Seed data into your database
def seed_items():
    for item in items:
        product = Item(
            item_name=item.item_name,
            description=item.description,
            price=item.price,
            category=item.category,
            items_available=item.items_available,
            image_url=item.image_url
        )
        db.session.add(product)
    
    db.session.commit()

# Run the seed function
if __name__ == "__main__":
    seed_items()
