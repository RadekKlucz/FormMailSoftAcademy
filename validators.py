import re
import html
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FormValidator:
    def __init__(self):
        # Email regex pattern
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        # Phone regex pattern (global format: +country code followed by digits, spaces, hyphens, or parentheses, 7 to 15 digits total)
        self.phone_pattern = re.compile(r'^(\+|00)[1-9][0-9]{6,14}$')

    def validate_contact_form(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate contact form data"""
        errors = []
        cleaned_data = {}

        # Validate name
        name = self._sanitize_string(data.get('name', ''))
        if not name or len(name.strip()) < 2:
            errors.append('Imię jest wymagane (minimum 2 znaki)')
        elif len(name) > 100:
            errors.append('Imię jest zbyt długie (maksimum 100 znaków)')
        else:
            cleaned_data['name'] = name

        # Validate contact method
        contact_method = data.get('contact_method', '')
        if contact_method not in ['email', 'phone']:
            errors.append('Wybierz preferowaną metodę kontaktu')
        else:
            cleaned_data['contact_method'] = contact_method

        # Validate language
        language = data.get('language', 'pl')
        if language not in ['pl', 'en']:
            errors.append('Nieprawidłowy język')
        else:
            cleaned_data['language'] = language

        # Validate email (optional but must be valid if provided)
        email = self._sanitize_email(data.get('email', ''))
        if email and not self.email_pattern.match(email):
            errors.append('Podaj prawidłowy adres e-mail')
        elif email and len(email) > 254:
            errors.append('Adres e-mail jest zbyt długi')

        if email:
            cleaned_data['email'] = email

        # Validate phone (optional but must be valid if provided)
        phone = self._sanitize_string(data.get('phone', ''))
        if phone and not self.phone_pattern.match(phone):
            errors.append('Podaj prawidłowy numer telefonu (format: +kod_kraju numer)')
        elif phone and len(phone) > 20:
            errors.append('Numer telefonu jest zbyt długi')

        if phone:
            cleaned_data['phone'] = phone

        # Ensure at least one contact method is provided
        if not email and not phone:
            errors.append('Podaj przynajmniej jeden sposób kontaktu (email lub telefon)')

        # Validate message (optional)
        message = self._sanitize_text(data.get('message', ''))
        if message and len(message) > 2000:
            errors.append('Wiadomość jest zbyt długa (maksimum 2000 znaków)')

        # Always include message in cleaned data, even if empty
        cleaned_data['message'] = message if message else ''

        # Check for suspicious content
        if self._detect_spam(data):
            errors.append('Wiadomość została odrzucona')

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'data': cleaned_data if len(errors) == 0 else {}
        }

    def validate_reservation_form(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate reservation form data"""
        errors = []
        cleaned_data = {}

        # Validate name
        name = self._sanitize_string(data.get('name', ''))
        if not name or len(name.strip()) < 2:
            errors.append('Imię jest wymagane (minimum 2 znaki)')
        elif len(name) > 100:
            errors.append('Imię jest zbyt długie (maksimum 100 znaków)')
        else:
            cleaned_data['name'] = name

        # Validate contact method
        contact_method = data.get('contact_method', '')
        if contact_method not in ['email', 'phone']:
            errors.append('Wybierz preferowaną metodę kontaktu')
        else:
            cleaned_data['contact_method'] = contact_method

        # Validate language
        language = data.get('language', 'pl')
        if language not in ['pl', 'en']:
            errors.append('Nieprawidłowy język')
        else:
            cleaned_data['language'] = language

        # Validate email (optional but must be valid if provided)
        email = self._sanitize_email(data.get('email', ''))
        if email and not self.email_pattern.match(email):
            errors.append('Podaj prawidłowy adres e-mail')
        elif email and len(email) > 254:
            errors.append('Adres e-mail jest zbyt długi')

        if email:
            cleaned_data['email'] = email

        # Validate phone (optional but must be valid if provided)
        phone = self._sanitize_string(data.get('phone', ''))
        if phone and not self.phone_pattern.match(phone):
            errors.append('Podaj prawidłowy numer telefonu (format: +kod_kraju numer)')
        elif phone and len(phone) > 20:
            errors.append('Numer telefonu jest zbyt długi')

        if phone:
            cleaned_data['phone'] = phone

        # Ensure at least one contact method is provided
        if not email and not phone:
            errors.append('Podaj przynajmniej jeden sposób kontaktu (email lub telefon)')

        # Validate service (optional for reservation)
        service = self._sanitize_string(data.get('service', ''))
        if service and len(service) > 200:
            errors.append('Nazwa usługi jest zbyt długa')

        # Always include service in cleaned data, even if empty
        cleaned_data['service'] = service if service else ''

        # Validate additional info (optional) - this is the message field for reservations
        additional_info = self._sanitize_text(data.get('additional_info', ''))
        if additional_info and len(additional_info) > 2000:
            errors.append('Dodatkowe informacje są zbyt długie (maksimum 2000 znaków)')

        # Always include additional_info in cleaned data, even if empty
        cleaned_data['additional_info'] = additional_info if additional_info else ''

        # Check for suspicious content
        if self._detect_spam(data):
            errors.append('Rezerwacja została odrzucona')

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'data': cleaned_data if len(errors) == 0 else {}
        }

    def _sanitize_string(self, value: str) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            return ''

        # Remove HTML tags and decode HTML entities
        cleaned = html.escape(value.strip())
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned

    def _sanitize_email(self, value: str) -> str:
        """Sanitize email input"""
        if not isinstance(value, str):
            return ''

        # Convert to lowercase and strip whitespace
        email = value.lower().strip()
        # Remove any HTML tags
        email = html.escape(email)
        return email

    def _sanitize_text(self, value: str) -> str:
        """Sanitize text area input (preserve line breaks)"""
        if not isinstance(value, str):
            return ''

        # Remove HTML tags but preserve line breaks
        cleaned = html.escape(value.strip())
        # Normalize line breaks
        cleaned = re.sub(r'\r\n|\r', '\n', cleaned)
        # Limit consecutive line breaks
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        return cleaned

    def _detect_spam(self, data: Dict[str, Any]) -> bool:
        """Basic spam detection"""
        spam_indicators = [
            'http://', 'https://', 'www.', '.com', '.net', '.org',
            'viagra', 'casino', 'poker', 'loan', 'credit',
            'make money', 'work from home', 'click here',
            'free money', 'guaranteed', '100%'
        ]

        # Check all text fields for spam indicators
        text_fields = ['name', 'message', 'additional_info']

        for field in text_fields:
            value = data.get(field, '')
            if isinstance(value, str):
                value_lower = value.lower()

                # Check for spam keywords
                spam_count = sum(1 for indicator in spam_indicators if indicator in value_lower)
                if spam_count >= 2:
                    logger.warning(f"Spam detected in field '{field}': {spam_count} indicators")
                    return True

                # Check for excessive URLs/links
                url_count = len(re.findall(r'http[s]?://|www\.|\.[a-z]{2,4}/', value_lower))
                if url_count >= 2:
                    logger.warning(f"Excessive URLs detected in field '{field}': {url_count}")
                    return True

                # Check for excessive capitalization
                if len(value) > 10:
                    caps_ratio = sum(1 for c in value if c.isupper()) / len(value)
                    if caps_ratio > 0.6:
                        logger.warning(f"Excessive capitalization in field '{field}': {caps_ratio:.2f}")
                        return True

        return False