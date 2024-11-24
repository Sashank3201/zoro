# Zoro - Document Management Platform

A secure web application for storing and managing educational PDF documents with comprehensive admin controls and user-friendly interfaces.

## Features

- User Authentication and Role Management
- Document Upload and Management (Admin Only)
- Document Search by Year and Semester
- Modern, Responsive Dashboard
- Control Panel for System Administration
- Role-based Access Control
- Document Expiration System
- Mobile-First Design with Bootstrap 5

## Tech Stack

- Backend: Python Flask
- Frontend: HTML5, Bootstrap 5
- ORM: SQLAlchemy
- Authentication: Flask-Login
- Database: SQLite
- Deployment: Render

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zoro.git
cd zoro
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/pdf_portal.db
UPLOAD_FOLDER=uploads
```

5. Initialize the database and create uploads directory:
```bash
mkdir instance
mkdir uploads
flask db upgrade
```

6. Create an admin user:
```bash
python create_admin.py
```

7. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Deployment on Render

### 1. Prerequisites
- A GitHub account
- Your code pushed to a GitHub repository
- A Render account (https://render.com)

### 2. Configuration Files
The repository includes necessary configuration files:

- `render.yaml`: Deployment configuration
- `requirements.txt`: Python dependencies
- `Procfile`: Process configuration
- `wsgi.py`: WSGI configuration

### 3. Deployment Steps

1. Log in to Render Dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: zoro-document-portal
   - Environment: Python
   - Region: Choose nearest
   - Branch: main
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`

### 4. Environment Variables

Set these in Render dashboard:
```
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=[generate a secure key]
DATABASE_URL=sqlite:///instance/pdf_portal.db
UPLOAD_FOLDER=uploads
```

### 5. Persistent Storage

Configure disk storage:
- Name: uploads
- Mount Path: /opt/render/project/src/uploads
- Size: 1GB

### 6. Post-Deployment

1. Create admin user:
   - Use Render Shell
   - Run: `python create_admin.py`
2. Monitor logs for any issues
3. Test all functionality
4. Set up regular backups

## Default Admin Credentials

- Email: sashank3301@gmail.com
- Password: sashank123

**Important:** Change these credentials immediately after first login.

## Security Features

- Password hashing with Werkzeug
- CSRF protection
- Secure file upload handling
- Role-based access control
- Session management
- Input validation and sanitization
- Secure headers configuration

## Maintenance

### Regular Tasks
- Monitor log files in `logs/zoro_portal.log`
- Check disk usage for uploads
- Review expired documents
- Backup database regularly

### Backup Strategy
1. Database: Daily automated backups
2. Uploaded files: Regular syncs
3. Configuration: Version controlled

## Troubleshooting

### Common Issues

1. Upload Issues
   - Check disk space
   - Verify folder permissions
   - Check file size limits

2. Database Issues
   - Verify connection string
   - Check file permissions
   - Monitor disk space

3. Authentication Issues
   - Clear browser cache
   - Check session configuration
   - Verify user permissions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
