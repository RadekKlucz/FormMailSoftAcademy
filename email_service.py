import os
import json
import smtplib
import logging
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Konfiguracja serwera SMTP Gmail
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # UWAGA: Skonfiguruj te zmienne środowiskowe w swoim środowisku hostingowym:
        # 
        # GMAIL_EMAIL - Twój adres Gmail (np. "twoja-firma@gmail.com")
        # Aby uzyskać ten adres:
        # 1. Utwórz lub użyj istniejącego konta Gmail
        # 2. Ustaw ten adres jako nadawcę wiadomości

        # GMAIL_APP_PASSWORD - Hasło aplikacji Gmail (NIE zwykłe hasło!)
        # Aby uzyskać hasło aplikacji:
        # 1. Przejdź do https://myaccount.google.com/security
        # 2. Włącz uwierzytelnianie dwuetapowe jeśli nie jest włączone
        # 3. Przejdź do "Hasła aplikacji" (App Passwords)
        # 4. Wygeneruj nowe hasło dla "Mail"
        # 5. Użyj wygenerowanego 16-znakowego kodu (bez spacji)

        # RECIPIENT_EMAIL - Adres, na który będą wysyłane formularze (np. "kontakt@twoja-firma.com")
        # To może być ten sam adres co GMAIL_EMAIL lub inny

        self.sender_email = os.getenv("GMAIL_EMAIL", "your-email@gmail.com")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD", "your-app-password") 
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", self.sender_email)

        # Load translations
        self.translations = self._load_translations()

    def _load_translations(self):
        """Load translations from JSON file"""
        try:
            with open('translations.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load translations: {str(e)}")
            # Fallback to empty dict if file not found
            return {"pl": {"contact": {}, "reservation": {}}, "en": {"contact": {}, "reservation": {}}}

    def _get_labels(self, language, form_type):
        """Get translated labels for specific language and form type"""
        lang = language if language in self.translations else 'pl'
        return self.translations.get(lang, {}).get(form_type, {})

    def _generate_unique_id(self, name):
        """Generate unique ID for email subject to prevent threading"""
        # Format: #ddMMRRRR{first_letter}{last_letter}unique_chars
        timestamp = datetime.now().strftime("%d%m%Y")  # ddMMRRRR format

        # Extract first and last letter from name
        clean_name = ''.join(c.upper() for c in name if c.isalpha())
        if len(clean_name) >= 2:
            first_letter = clean_name[0]
            last_letter = clean_name[-1]
        elif len(clean_name) == 1:
            first_letter = last_letter = clean_name[0]
        else:
            first_letter = last_letter = 'X'

        # Generate unique characters (4 random hex characters)
        unique_part = secrets.token_hex(2).upper()

        return f"#{timestamp}{first_letter}{last_letter}{unique_part}"

    def test_connection(self):
        """Test SMTP connection"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False

    def send_contact_email(self, form_data):
        """Send contact form email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            unique_id = self._generate_unique_id(form_data['name'])
            language = form_data.get('language', 'pl')
            labels = self._get_labels(language, 'contact')

            # Bilingual subject
            subject = f"{labels.get('title', 'New contact message')} - {form_data['name']} {unique_id}"

            msg['Subject'] = subject
            msg['From'] = formataddr((labels.get('form_name', 'Contact Form'), self.sender_email))
            msg['To'] = self.recipient_email
            msg['Reply-To'] = form_data['email']

            # Create email body
            html_body = self._create_email_html(form_data, 'contact')
            text_body = self._create_email_text(form_data, 'contact')

            # Attach parts
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"Contact email sent successfully for {form_data['name']}")
            return {'success': True}

        except Exception as e:
            logger.error(f"Failed to send contact email: {str(e)}")
            return {'success': False, 'error': str(e)}

    def send_reservation_email(self, form_data):
        """Send reservation form email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            unique_id = self._generate_unique_id(form_data['name'])
            language = form_data.get('language', 'pl')
            labels = self._get_labels(language, 'reservation')

            # Bilingual subject
            subject = f"{labels.get('title', 'New reservation')} - {form_data['name']} {unique_id}"

            msg['Subject'] = subject
            msg['From'] = formataddr((labels.get('form_name', 'Reservation Form'), self.sender_email))
            msg['To'] = self.recipient_email
            msg['Reply-To'] = form_data['email']

            # Create email body
            html_body = self._create_email_html(form_data, 'reservation')
            text_body = self._create_email_text(form_data, 'reservation')

            # Attach parts
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"Reservation email sent successfully for {form_data['name']}")
            return {'success': True}

        except Exception as e:
            logger.error(f"Failed to send reservation email: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _create_email_html(self, data, form_type):
        """Create HTML email body for any form type"""
        language = data.get('language', 'pl')
        labels = self._get_labels(language, form_type)

        preferred_contact = labels.get('contact_email', 'Email') if data['contact_method'] == 'email' else labels.get('contact_phone', 'Phone')
        contact_lang_display = labels.get('lang_en', 'English') if language == 'en' else labels.get('lang_pl', 'Polish')
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Base HTML template
        html_header = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {'#e8f5e8' if form_type == 'reservation' else '#f8f9fa'}; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #555; }}
                .value {{ margin-top: 5px; }}
                .highlight {{ background-color: #fff3cd; padding: 10px; border-radius: 3px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{labels.get('title', 'New message')}</h2>
                    <p>{labels.get('received', 'Received')}: {timestamp}</p>
                </div>

                <div class="field {'highlight' if form_type == 'reservation' else ''}">
                    <div class="label">{labels.get('name', 'Name')}:</div>
                    <div class="value">{data['name']}</div>
                </div>

                <div class="field">
                    <div class="label">{labels.get('contact_method', 'Contact method')}:</div>
                    <div class="value">{preferred_contact}</div>
                </div>

                <div class="field">
                    <div class="label">{labels.get('contact_language', 'Language')}:</div>
                    <div class="value">{contact_lang_display}</div>
                </div>

                <div class="field">
                    <div class="label">{labels.get('email', 'Email')}:</div>
                    <div class="value">{data['email']}</div>
                </div>
        """

        # Add phone field if present
        if data.get('phone'):
            html_header += f"""
                <div class="field">
                    <div class="label">{labels.get('phone', 'Phone')}:</div>
                    <div class="value">{data['phone']}</div>
                </div>
            """

        # Add form-specific fields
        if form_type == 'contact' and data.get('message'):
            html_header += f"""
                <div class="field">
                    <div class="label">{labels.get('message', 'Message')}:</div>
                    <div class="value">{data['message'].replace(chr(10), '<br>')}</div>
                </div>
            """
        elif form_type == 'reservation':
            if data.get('service'):
                html_header += f"""
                <div class="field">
                    <div class="label">{labels.get('service', 'Service')}:</div>
                    <div class="value">{data['service']}</div>
                </div>
                """
            if data.get('additional_info'):
                html_header += f"""
                <div class="field">
                    <div class="label">{labels.get('additional_info', 'Additional info')}:</div>
                    <div class="value">{data['additional_info'].replace(chr(10), '<br>')}</div>
                </div>
                """

        # Footer
        if form_type == 'reservation':
            html_footer = f"""
                <div class="footer">
                    <p>{labels.get('footer1', 'Automatic message')}</p>
                    <p><strong>{labels.get('footer2', 'Confirm reservation!')}</strong></p>
                </div>
            </div>
        </body>
        </html>
            """
        else:
            html_footer = f"""
                <div class="footer">
                    <p>{labels.get('footer', 'Automatic message')}</p>
                </div>
            </div>
        </body>
        </html>
            """

        return html_header + html_footer

    def _create_email_text(self, data, form_type):
        """Create plain text email body for any form type"""
        language = data.get('language', 'pl')
        labels = self._get_labels(language, form_type)

        preferred_contact = labels.get('contact_email', 'Email') if data['contact_method'] == 'email' else labels.get('contact_phone', 'Phone')
        contact_lang_display = labels.get('lang_en', 'English') if language == 'en' else labels.get('lang_pl', 'Polish')
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        text = f"""
{labels.get('title', 'NEW MESSAGE').upper()}
{labels.get('received', 'Received')}: {timestamp}

{labels.get('name', 'Name')}: {data['name']}
{labels.get('contact_method', 'Contact method')}: {preferred_contact}
{labels.get('contact_language', 'Language')}: {contact_lang_display}
{labels.get('email', 'Email')}: {data['email']}
"""

        if data.get('phone'):
            text += f"{labels.get('phone', 'Phone')}: {data['phone']}\n"

        # Add form-specific fields
        if form_type == 'contact' and data.get('message'):
            text += f"\n{labels.get('message', 'Message')}:\n{data['message']}\n"
        elif form_type == 'reservation':
            if data.get('service'):
                text += f"{labels.get('service', 'Service')}: {data['service']}\n"
            if data.get('additional_info'):
                text += f"\n{labels.get('additional_info', 'Additional info')}:\n{data['additional_info']}\n"

        # Footer
        if form_type == 'reservation':
            text += f"\n---\n{labels.get('footer1', 'Automatic message')}"
            text += f"\n{labels.get('footer2', 'CONFIRM RESERVATION!').upper()}"
        else:
            text += f"\n---\n{labels.get('footer', 'Automatic message')}"

        return text