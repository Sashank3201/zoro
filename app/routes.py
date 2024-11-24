from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file, current_app, send_from_directory
from flask_login import login_required, current_user
from app import db
from app.models import Document, User
from functools import wraps
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get document statistics
        total_documents = Document.query.filter_by(user_id=current_user.id).count()
        active_documents = Document.query.filter(
            Document.user_id == current_user.id,
            Document.expiration_date > datetime.utcnow()
        ).count()
        current_year = datetime.utcnow().year

        return render_template('dashboard.html',
                             total_documents=total_documents,
                             active_documents=active_documents,
                             current_year=current_year)
    except Exception as e:
        flash('An error occurred while loading the dashboard.', 'danger')
        return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('main.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main.route('/signup', methods=['GET'])
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

    new_user = User(email=email, name=name)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! Please log in.', 'success')
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
    documents = query.all()
    
    # Get unique years and semesters for filter dropdowns
    years = sorted(list(set(doc.year for doc in Document.query.all())))
    semesters = sorted(list(set(doc.semester for doc in Document.query.all())))
    
    return render_template('documents.html', 
                         documents=documents,
                         years=years,
                         semesters=semesters)

@main.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
@login_required
def upload_post():
    try:
        if 'pdf' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('main.upload'))

        file = request.files['pdf']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('main.upload'))

        if not file.filename.endswith('.pdf'):
            flash('Only PDF files are allowed', 'danger')
            return redirect(url_for('main.upload'))

        year = request.form.get('year')
        semester = request.form.get('semester')

        if not year or not semester:
            flash('Please provide both year and semester', 'danger')
            return redirect(url_for('main.upload'))

        try:
            year = int(year)
            semester = int(semester)
        except ValueError:
            flash('Invalid year or semester value', 'danger')
            return redirect(url_for('main.upload'))

        if semester < 1 or semester > 8:
            flash('Semester must be between 1 and 8', 'danger')
            return redirect(url_for('main.upload'))

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file.filename)
        filename = f"{timestamp}_{original_filename}"

        # Save file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Create document record
        document = Document(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            year=year,
            semester=semester,
            user_id=current_user.id,
            expiration_date=datetime.utcnow() + timedelta(days=2)
        )

        db.session.add(document)
        db.session.commit()

        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('main.documents'))

    except Exception as e:
        flash('An error occurred while uploading the document.', 'danger')
        return redirect(url_for('main.upload'))

@main.route('/delete_document/<int:doc_id>')
@login_required
def delete_document(doc_id):
    try:
        doc = Document.query.get_or_404(doc_id)
        
        # Check if user owns the document
        if doc.user_id != current_user.id:
            flash('You do not have permission to delete this document.', 'danger')
            return redirect(url_for('main.documents'))
            
        # Delete physical file
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
            
        # Delete database record
        db.session.delete(doc)
        db.session.commit()
        flash(f'Document {doc.original_filename} has been deleted.', 'success')
    except Exception as e:
        flash('An error occurred while deleting the document.', 'danger')
        
    return redirect(url_for('main.documents'))

@main.route('/download/<int:document_id>')
@login_required
def download(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        
        # Check if user owns the document
        if document.user_id != current_user.id:
            flash('You do not have permission to download this document.', 'danger')
            return redirect(url_for('main.documents'))
        
        # Check if file exists
        if not os.path.exists(document.file_path):
            flash('Document file not found.', 'danger')
            return redirect(url_for('main.documents'))
        
        # Check expiration
        if document.expiration_date and document.expiration_date < datetime.utcnow():
            flash('This document has expired.', 'danger')
            return redirect(url_for('main.documents'))
        
        return send_file(
            document.file_path,
            as_attachment=True,
            download_name=document.original_filename
        )
        
    except Exception as e:
        flash('An error occurred while downloading the document.', 'danger')
        return redirect(url_for('main.documents'))
