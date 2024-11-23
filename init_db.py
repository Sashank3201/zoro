from app import create_app, db
from app.models import User, Document
import os

def init_db():
    app = create_app()
    
    # Make sure the database file doesn't exist
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'pdf_portal.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create admin user
        admin = User(
            email='admin@pdfportal.com',
            name='Administrator',
            is_admin=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("Database initialized with admin user:")
        print("Email: admin@pdfportal.com")
        print("Password: admin123")

if __name__ == "__main__":
    init_db()
