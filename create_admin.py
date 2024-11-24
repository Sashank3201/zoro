from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Delete existing admin if exists
        admin = User.query.filter_by(email='admin@zoro.com').first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            print("Removed existing admin user")
        
        # Create new admin user
        admin = User(
            email='admin@zoro.com',
            name='Admin',
            is_admin=True,
            password=generate_password_hash('Admin@123')
        )
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("\nAdmin Credentials:")
        print("Email: admin@zoro.com")
        print("Password: Admin@123")

if __name__ == '__main__':
    create_admin_user()
