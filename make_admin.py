from app import create_app, db
from app.models import User

def make_user_admin():
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email='sashank3301@gmail.com').first()
        if not user:
            print("User not found!")
            return
        
        user.is_admin = True
        db.session.commit()
        print(f"Successfully made {user.email} an admin!")

if __name__ == '__main__':
    make_user_admin()
