from app import create_app, db
from app.models import User, Document
import os
import shutil

def cleanup():
    app = create_app()
    with app.app_context():
        print("Cleaning up database and files...")
        
        # Drop all tables
        db.drop_all()
        print("Dropped all tables")
        
        # Recreate tables
        db.create_all()
        print("Recreated empty tables")
        
        # Clean up uploads directory
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        if os.path.exists(uploads_dir):
            try:
                shutil.rmtree(uploads_dir)
                print(f"Deleted uploads directory: {uploads_dir}")
            except Exception as e:
                print(f"Error deleting uploads directory: {e}")
        
        print("Cleanup completed successfully!")

if __name__ == "__main__":
    cleanup()
