from models import db, User, Clothes, WhatsNew, FlashSale, HotInCategory, Artwork, Shoes, Electronics, Book, Cart, CartItem
from app import app  
from datetime import datetime

# Create all tables in the database
with app.app_context():
    db.drop_all()  # Drops all tables if they exist (for testing purposes)
    db.create_all()  # Creates new tables


# Function to seed the database with GroupThree user and initial data
def seed_data():
    # Create GroupThree User
    groupthree_user = User(name="GroupThree", email="groupthree@gmail.com", password="groupthreepassword")

    # Add user to the session
    db.session.add(groupthree_user)

    # Create Clothes
    clothes1 = Clothes(name="T-Shirt", description="A cool t-shirt", price=19.99, image_url="tshirt.jpg")
    clothes2 = Clothes(name="Jeans", description="Stylish jeans", price=49.99, image_url="jeans.jpg")

    # Create WhatsNew items
    whats_new1 = WhatsNew(title="New Collection!", description="Check out our latest collection", 
                         image_url="new_collection.jpg", release_date=datetime(2024, 1, 1))

    # Create FlashSale items
    flash_sale1 = FlashSale(name="50% off on Shoes", discount=50.0, 
                            start_time=datetime(2024, 10, 1, 10, 0), end_time=datetime(2024, 10, 2, 10, 0))

    # Create HotInCategory items
    hot_in_category1 = HotInCategory(category="Clothes", product_id=1)  # Assuming '1' is the ID of the first Clothes item

    # Create Artwork
    artwork1 = Artwork(title="Sunset Painting", artist_name="Vincent", image_url="sunset.jpg", price=1500.00)

    # Create Shoes
    shoes1 = Shoes(name="Running Shoes", size="42", price=719.99, image_url="shoes.jpg")

    # Create Electronics
    electronics1 = Electronics(name="Smartphone", description="Latest model smartphone", price=799.99, image_url="phone.jpg")

    # Create Books
    book1 = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", description="Classic novel", price=999.99, image_url="gatsby.jpg")

    # Add all products to the session
    db.session.add_all([clothes1, clothes2, whats_new1, flash_sale1, hot_in_category1, artwork1, shoes1, electronics1, book1])

    # Commit the session to save the data
    db.session.commit()

    # Create a cart for GroupThree
    cart1 = Cart(user_id=groupthree_user.id)
    db.session.add(cart1)
    db.session.commit()

    # Add items to the cart
    cart_item1 = CartItem(cart_id=cart1.id, product_type="clothes", product_id=clothes1.id, quantity=2)
    cart_item2 = CartItem(cart_id=cart1.id, product_type="books", product_id=book1.id, quantity=1)
    cart_item3 = CartItem(cart_id=cart1.id, product_type="shoes", product_id=shoes1.id, quantity=1)

    # Add cart items to the session
    db.session.add_all([cart_item1, cart_item2, cart_item3])

    # Commit the session to save the cart items
    db.session.commit()

    print("Database seeded successfully for GroupThree!")


if __name__ == '__main__':
    with app.app_context():
        seed_data()
