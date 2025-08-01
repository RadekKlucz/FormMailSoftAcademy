import os
import logging
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from email_service import EmailService
from validators import FormValidator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# UWAGA: Ustaw SESSION_SECRET w zmiennych środowiskowych
# To powinien być losowy, bezpieczny klucz dla szyfrowania sesji
# Możesz wygenerować klucz używając: python -c "import secrets; print(secrets.token_hex(32))"
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure CORS
# UWAGA: W produkcji zmień origins=["*"] na konkretne domeny
# Przykład: origins=["https://twoja-strona.netlify.app", "https://twoja-domena.com"]
CORS(app, origins=["*"])

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per hour"]
)

# Initialize services
email_service = EmailService()
form_validator = FormValidator()

# API Security Configuration
# UWAGA: Ustaw API_SECRET_KEY w zmiennych środowiskowych jako długi, losowy klucz
# Wygeneruj klucz: python -c "import secrets; print(secrets.token_hex(32))"
API_SECRET_KEY = os.environ.get("API_SECRET_KEY", "dev-api-key-change-in-production")

def verify_api_signature(request_data, signature):
    """Verify HMAC signature for API security"""
    if not signature:
        return False
    
    try:
        # Create expected signature
        request_string = str(request_data).encode('utf-8')
        expected_signature = hmac.new(
            API_SECRET_KEY.encode('utf-8'),
            request_string,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures safely
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Error verifying API signature: {str(e)}")
        return False

def generate_api_key():
    """Generate new API key for client"""
    return secrets.token_hex(32)

@app.route('/api/generate-key', methods=['POST'])
@limiter.limit("1 per hour")
def generate_key():
    """Generate API key for authenticated requests (protected endpoint)"""
    # Simple authentication - in production use proper auth
    auth_token = request.headers.get('Authorization')
    if auth_token != f"Bearer {API_SECRET_KEY}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    new_key = generate_api_key()
    return jsonify({
        'api_key': new_key,
        'usage': 'Include in X-API-Key header for authenticated requests'
    }), 200

@app.route('/')
def index():
    """Main page with form documentation"""
    return render_template('index.html')

@app.route('/test')
def test_forms():
    """Test page with sample forms"""
    return render_template('test_forms.html')

@app.route('/api/contact', methods=['POST'])
@limiter.limit("5 per minute")  # Strict rate limiting for contact form
def contact_form():
    """Handle contact form submissions"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Optional API Key authentication (if provided)
        api_key = request.headers.get('X-API-Key')
        if api_key:
            # If API key is provided, verify it
            signature = request.headers.get('X-Signature')
            if not verify_api_signature(data, signature):
                return jsonify({'error': 'Invalid API signature'}), 401

        # Validate form data
        validation_result = form_validator.validate_contact_form(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['errors']}), 400

        # Check for honeypot (spam protection)
        if data.get('website') or data.get('url'):  # Common honeypot field names
            logger.warning(f"Honeypot triggered from IP: {get_remote_address()}")
            return jsonify({'error': 'Invalid submission'}), 400

        # Send email
        email_result = email_service.send_contact_email(validation_result['data'])
        if not email_result['success']:
            logger.error(f"Failed to send contact email: {email_result['error']}")
            return jsonify({'error': 'Failed to send message'}), 500

        logger.info(f"Contact form submitted successfully from IP: {get_remote_address()}")
        return jsonify({'message': 'Message sent successfully'}), 200

    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/reservation', methods=['POST'])
@limiter.limit("3 per minute")  # Even stricter rate limiting for reservations
def reservation_form():
    """Handle reservation form submissions"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Optional API Key authentication (if provided)
        api_key = request.headers.get('X-API-Key')
        if api_key:
            # If API key is provided, verify it
            signature = request.headers.get('X-Signature')
            if not verify_api_signature(data, signature):
                return jsonify({'error': 'Invalid API signature'}), 401

        # Validate form data
        validation_result = form_validator.validate_reservation_form(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['errors']}), 400

        # Check for honeypot (spam protection)
        if data.get('website') or data.get('url'):
            logger.warning(f"Honeypot triggered from IP: {get_remote_address()}")
            return jsonify({'error': 'Invalid submission'}), 400

        # Send email
        email_result = email_service.send_reservation_email(validation_result['data'])
        if not email_result['success']:
            logger.error(f"Failed to send reservation email: {email_result['error']}")
            return jsonify({'error': 'Failed to send reservation'}), 500

        logger.info(f"Reservation form submitted successfully from IP: {get_remote_address()}")
        return jsonify({'message': 'Reservation sent successfully'}), 200

    except Exception as e:
        logger.error(f"Error processing reservation form: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'email_service': email_service.test_connection()
    }), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
