from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file, current_app, send_from_directory
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models import Document, User
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('main.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))

@main.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('signup.html')

@main.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists', 'danger')
        return redirect(url_for('main.signup'))

    # Create new user with is_admin=True if it's the first user
    is_admin = User.query.count() == 0
    
    new_user = User(email=email, name=name, is_admin=is_admin)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.login'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/documents')
@login_required
def documents():
    # Get search parameters
    year = request.args.get('year')
    semester = request.args.get('semester')
    
    # Build query
    query = Document.query
    
    # Apply filters if provided
    if year:
        query = query.filter_by(year=year)
    if semester:
        query = query.filter_by(semester=semester)
        
    # Get all documents
    documents = query.order_by(Document.upload_date.desc()).all()
    return render_template('documents.html', documents=documents)

@main.route('/upload')
@login_required
@admin_required
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
@login_required
@admin_required
def upload_post():
    try:
        if 'pdf_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('main.upload'))
        
        file = request.files['pdf_file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('main.upload'))

        if not file.filename.endswith('.pdf'):
            flash('Only PDF files are allowed', 'danger')
            return redirect(url_for('main.upload'))

        year = request.form.get('year')
        semester = request.form.get('semester')
        
        if not year or not semester:
            flash('Year and semester are required', 'danger')
            return redirect(url_for('main.upload'))

        # Create a unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        
        # Save the file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(f"Attempting to save file to: {file_path}")  # Debug log
        
        try:
            file.save(file_path)
            print(f"File saved successfully to: {file_path}")  # Debug log
        except Exception as save_error:
            print(f"Error saving file: {str(save_error)}")  # Debug log
            raise save_error

        # Create document record
        document = Document(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,  # Add the file path
            year=int(year),
            semester=int(semester),
            owner=current_user,
            upload_date=datetime.utcnow(),
            expiration_date=datetime.utcnow() + timedelta(days=2)
        )
        
        db.session.add(document)
        db.session.commit()
        print(f"Document record created successfully: {document.id}")  # Debug log
        
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('main.documents'))
        
    except Exception as e:
        print(f"Upload error: {str(e)}")  # Debug log
        db.session.rollback()
        flash(f'Error uploading document: {str(e)}', 'danger')
        return redirect(url_for('main.upload'))

@main.route('/download/<int:document_id>')
@login_required
def download(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        
        if document.is_expired():
            flash('This document has expired and is no longer available for download.', 'warning')
            return redirect(url_for('main.documents'))
            
        print(f"Attempting to download file: {document.filename}")  # Debug log
        print(f"File path: {os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename)}")  # Debug log
        
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename)):
            print(f"File not found in uploads directory")  # Debug log
            flash('File not found in the system.', 'danger')
            return redirect(url_for('main.documents'))
            
        try:
            return send_file(
                os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename),
                download_name=document.original_filename,
                as_attachment=True
            )
        except Exception as e:
            print(f"Error sending file: {str(e)}")  # Debug log
            raise e
            
    except Exception as e:
        print(f"Download error: {str(e)}")  # Debug log
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('main.documents'))

@main.route('/delete/<int:document_id>')
@login_required
@admin_required
def delete(document_id):
    document = Document.query.get_or_404(document_id)
    
    if document.owner != current_user and not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('main.documents'))
    
    try:
        # Delete the physical file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the database record
        db.session.delete(document)
        db.session.commit()
        
        flash('Document deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Error removing document: ' + str(e))
    
    return redirect(url_for('main.documents'))

@main.route('/admin')
@login_required
@admin_required
def admin_panel():
    users = User.query.all()
    documents = Document.query.all()
    return render_template('admin.html', users=users, documents=documents)

@main.route('/admin/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('main.admin_panel'))
    
    user = User.query.get_or_404(user_id)
    
    # Delete user's documents
    for doc in user.documents:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.email} has been deleted', 'success')
    return redirect(url_for('main.admin_panel'))

@main.route('/admin/delete_document/<int:doc_id>')
@login_required
@admin_required
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    
    # Delete physical file
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(doc)
    db.session.commit()
    
    flash(f'Document {doc.original_filename} has been deleted', 'success')
    return redirect(url_for('main.admin_panel'))
