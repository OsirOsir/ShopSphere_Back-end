from models import db, User
from app import app  
from datetime import datetime

def seed_data():
    groupthree_user = User(name="GroupThree", email="groupthree@gmail.com")
    groupthree_user.password = "groupthreepassword"  # Set the password after initializing
    

    # Add user to the session
    db.session.add(groupthree_user)
    db.session.commit() 
    
    print("Database seeded successfully for GroupThree!")
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drops all tables (use with caution in production)
        db.create_all()  # Creates all tables
        seed_data()  # Calls the function to seed data
