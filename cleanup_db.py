import os
from app import create_app, db
from app.models import User, Document

def cleanup_database():
    print("Starting cleanup process...")
    
    # Create Flask app context
    app = create_app()
    with app.app_context():
        try:
            # Get all documents to delete their files first
            documents = Document.query.all()
            print(f"Found {len(documents)} documents to remove")
            
            # Delete physical files
            for doc in documents:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {doc.filename}")
            
            # Delete all documents from database
            Document.query.delete()
            print("Deleted all document records from database")
            
            # Delete all users
            num_users = User.query.count()
            User.query.delete()
            print(f"Deleted {num_users} users from database")
            
            # Commit the changes
            db.session.commit()
            print("Changes committed to database")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
            db.session.rollback()
            raise
        
        print("Cleanup completed successfully!")

if __name__ == '__main__':
    cleanup_database()
