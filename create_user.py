from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_user():
    app = create_app()
    with app.app_context():
        # Remove existing user if exists
        user = User.query.filter_by(email='sashank3301@gmail.com').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print("Removed existing user")
        
        # Create new user with admin privileges
        new_user = User(
            email='sashank3301@gmail.com',
            name='Sashank',
            password=generate_password_hash('sashank123'),
            is_admin=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        print("User created successfully with admin privileges!")
        print("\nCredentials:")
        print("Email: sashank3301@gmail.com")
        print("Password: sashank123")

if __name__ == '__main__':
    create_user()
