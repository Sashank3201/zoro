from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create a test user
    test_user = User(
        email='test2@example.com',  # Changed email
        name='Test User 2',
        password=generate_password_hash('test123', method='pbkdf2:sha256')
    )
    
    # Add to database
    db.session.add(test_user)
    db.session.commit()
    print("Test user created successfully!")
