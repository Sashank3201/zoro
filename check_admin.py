from app import create_app, db
from app.models import User

def check_admin():
    app = create_app()
    with app.app_context():
        # Check if admin user exists
        admin_user = User.query.filter_by(email='sashank3301@gmail.com').first()
        if admin_user:
            print("\nAdmin user found:")
            print(f"Email: {admin_user.email}")
            print(f"Is Admin: {admin_user.is_admin}")
            print(f"Name: {admin_user.name}")
        else:
            print("\nAdmin user not found!")
            
        # Show all users
        print("\nAll users in database:")
        users = User.query.all()
        for user in users:
            print(f"Email: {user.email}, Is Admin: {user.is_admin}")

if __name__ == '__main__':
    check_admin()
