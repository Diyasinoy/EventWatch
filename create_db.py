from app import app, db
from app.models import User, Event
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create all database tables
    db.create_all()
    
    # Create a test user
    test_user = User(
        email='test@example.com',
        username='Test User',
        user_type='admin',
        department='IT'
    )
    test_user.password_hash = generate_password_hash('password123')
    
    # Add the test user to the database
    db.session.add(test_user)
    db.session.commit()
    
    print("Database tables created successfully!")
    print("Test user created:")
    print("Email: test@example.com")
    print("Password: password123") 