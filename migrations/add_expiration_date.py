"""Add expiration date to documents

This migration adds an expiration_date column to the document table
and sets a 2-day expiration for all existing documents.
"""

from datetime import datetime, timedelta
from sqlalchemy import text, inspect
from app import db
from app.models import Document

def column_exists(table_name, column_name):
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade():
    # Add expiration_date column if it doesn't exist
    if not column_exists('document', 'expiration_date'):
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE document ADD COLUMN expiration_date DATETIME'))
            conn.commit()
    
    # Set expiration date for existing documents
    with db.session.begin():
        documents = Document.query.filter_by(expiration_date=None).all()
        for doc in documents:
            doc.expiration_date = datetime.utcnow() + timedelta(days=2)
        db.session.commit()

def downgrade():
    # Remove expiration_date column if it exists
    if column_exists('document', 'expiration_date'):
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE document DROP COLUMN expiration_date'))
            conn.commit()
