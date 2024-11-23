from app import db, create_app
from app.models import User

def upgrade():
    app = create_app()
    with app.app_context():
        # Add is_admin column
        with db.engine.connect() as conn:
            conn.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT FALSE')
            conn.execute('UPDATE user SET is_admin = FALSE')
            print("Added is_admin column to user table")

if __name__ == '__main__':
    upgrade()
