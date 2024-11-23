from app import create_app, db
from migrations.add_expiration_date import upgrade

app = create_app()

with app.app_context():
    upgrade()
    print("Migration completed successfully!")
