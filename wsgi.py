import os
import logging
from logging.handlers import RotatingFileHandler
from run import app

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/zoro_portal.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Zoro Document Portal startup')

if __name__ == "__main__":
    # Use environment variables with defaults
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
