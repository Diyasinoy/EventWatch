from app import app, db
from app.models import User, Event

def recreate_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database has been recreated!")

if __name__ == "__main__":
    recreate_database() 