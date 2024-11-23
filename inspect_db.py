from app import create_app, db
from app.models import User, Document

def inspect_database():
    app = create_app()
    with app.app_context():
        print("\n=== Database Tables ===")
        
        # Inspect User table
        print("\nTable: user")
        print("Columns: id, email, password, name")
        users = User.query.all()
        print("\nRows:")
        for user in users:
            print(f"({user.id}, '{user.email}', '{user.password}', '{user.name}')")
        
        # Inspect Document table
        print("\nTable: document")
        print("Columns: id, filename, original_filename, year, semester, upload_date, expiration_date, user_id, file_path")
        documents = Document.query.all()
        print("\nRows:")
        for doc in documents:
            print(f"({doc.id}, '{doc.filename}', '{doc.original_filename}', {doc.year}, {doc.semester}, "
                  f"'{doc.upload_date}', '{doc.expiration_date}', {doc.user_id}, '{doc.file_path}')")

if __name__ == "__main__":
    inspect_database()
