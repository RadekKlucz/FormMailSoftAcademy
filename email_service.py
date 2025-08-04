import os
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
            
            # Bilingual subject
            language = form_data.get('language', 'pl')
            if language == 'en':
                subject = f"New contact message - {form_data['name']} {unique_id}"
            else:
                subject = f"Nowa wiadomość kontaktowa - {form_data['name']} {unique_id}"
            
            msg['Subject'] = subject
            msg['From'] = formataddr(("Formularz Kontaktowy", self.sender_email))
            msg['To'] = self.recipient_email
            msg['Reply-To'] = form_data['email']

            # Create email body
            html_body = self._create_contact_email_html(form_data)
            text_body = self._create_contact_email_text(form_data)

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
            
            # Bilingual subject
            language = form_data.get('language', 'pl')
            if language == 'en':
                subject = f"New reservation - {form_data['name']} {unique_id}"
            else:
                subject = f"Nowa rezerwacja - {form_data['name']} {unique_id}"
            
            msg['Subject'] = subject
            msg['From'] = formataddr(("Formularz Rezerwacji", self.sender_email))
            msg['To'] = self.recipient_email
            msg['Reply-To'] = form_data['email']

            # Create email body
            html_body = self._create_reservation_email_html(form_data)
            text_body = self._create_reservation_email_text(form_data)

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

    def _create_contact_email_html(self, data):
        """Create HTML email body for contact form"""
        language = data.get('language', 'pl')
        
        # Bilingual field labels
        if language == 'en':
            labels = {
                'title': 'New Contact Message',
                'received': 'Received',
                'name': 'Name',
                'contact_method': 'Preferred contact method',
                'contact_language': 'Contact language',
                'email': 'Email address',
                'phone': 'Phone number',
                'message': 'Message',
                'footer': 'This message was sent automatically from the contact form on the website.',
                'contact_email': 'Email',
                'contact_phone': 'Phone',
                'lang_pl': 'Polish',
                'lang_en': 'English'
            }
        else:
            labels = {
                'title': 'Nowa wiadomość kontaktowa',
                'received': 'Otrzymano',
                'name': 'Imię i nazwisko',
                'contact_method': 'Preferowana metoda kontaktu',
                'contact_language': 'Język kontaktu',
                'email': 'Adres e-mail',
                'phone': 'Numer telefonu',
                'message': 'Wiadomość',
                'footer': 'Ta wiadomość została wysłana automatycznie z formularza kontaktowego na stronie internetowej.',
                'contact_email': 'E-mail',
                'contact_phone': 'Telefon',
                'lang_pl': 'Polski',
                'lang_en': 'English'
            }
        
        preferred_contact = labels['contact_email'] if data['contact_method'] == 'email' else labels['contact_phone']
        contact_lang_display = labels['lang_en'] if language == 'en' else labels['lang_pl']
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #555; }}
                .value {{ margin-top: 5px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{labels['title']}</h2>
                    <p>{labels['received']}: {timestamp}</p>
                </div>

                <div class="field">
                    <div class="label">{labels['name']}:</div>
                    <div class="value">{data['name']}</div>
                </div>

                <div class="field">
                    <div class="label">{labels['contact_method']}:</div>
                    <div class="value">{preferred_contact}</div>
                </div>

                <div class="field">
                    <div class="label">{labels['contact_language']}:</div>
                    <div class="value">{contact_lang_display}</div>
                </div>

                <div class="field">
                    <div class="label">{labels['email']}:</div>
                    <div class="value">{data['email']}</div>
                </div>

                {f'<div class="field"><div class="label">{labels["phone"]}:</div><div class="value">{data["phone"]}</div></div>' if data.get('phone') else ''}

                {f'<div class="field"><div class="label">{labels["message"]}:</div><div class="value">{data["message"].replace(chr(10), "<br>")}</div></div>' if data.get('message') else ''}

                <div class="footer">
                    <p>{labels['footer']}</p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_contact_email_text(self, data):
        """Create plain text email body for contact form"""
        language = data.get('language', 'pl')
        
        # Bilingual field labels
        if language == 'en':
            labels = {
                'title': 'NEW CONTACT MESSAGE',
                'received': 'Received',
                'name': 'Name',
                'contact_method': 'Preferred contact method',
                'contact_language': 'Contact language',
                'email': 'Email address',
                'phone': 'Phone number',
                'message': 'Message',
                'footer': 'This message was sent automatically from the contact form on the website.',
                'contact_email': 'Email',
                'contact_phone': 'Phone',
                'lang_pl': 'Polish',
                'lang_en': 'English'
            }
        else:
            labels = {
                'title': 'NOWA WIADOMOŚĆ KONTAKTOWA',
                'received': 'Otrzymano',
                'name': 'Imię i nazwisko',
                'contact_method': 'Preferowana metoda kontaktu',
                'contact_language': 'Język kontaktu',
                'email': 'Adres e-mail',
                'phone': 'Numer telefonu',
                'message': 'Wiadomość',
                'footer': 'Ta wiadomość została wysłana automatycznie z formularza kontaktowego na stronie internetowej.',
                'contact_email': 'E-mail',
                'contact_phone': 'Telefon',
                'lang_pl': 'Polski',
                'lang_en': 'English'
            }
        
        preferred_contact = labels['contact_email'] if data['contact_method'] == 'email' else labels['contact_phone']
        contact_lang_display = labels['lang_en'] if language == 'en' else labels['lang_pl']
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        text = f"""
{labels['title']}
{labels['received']}: {timestamp}

{labels['name']}: {data['name']}
{labels['contact_method']}: {preferred_contact}
{labels['contact_language']}: {contact_lang_display}
{labels['email']}: {data['email']}
"""

        if data.get('phone'):
            text += f"{labels['phone']}: {data['phone']}\n"

        if data.get('message'):
            text += f"\n{labels['message']}:\n{data['message']}\n"

        text += f"\n---\n{labels['footer']}"

        return text

    def _create_reservation_email_html(self, data):
        """Create HTML email body for reservation form"""
        language = data.get('language', 'pl')
        
        # Bilingual field labels
        if language == 'en':
            labels = {
                'title': 'New Reservation',
                'received': 'Received',
                'name': 'Name',
                'contact_method': 'Preferred contact method',
                'contact_language': 'Contact language',
                'email': 'Email address',
                'phone': 'Phone number',
                'service': 'Service',
                'additional_info': 'Additional information',
                'footer1': 'This reservation was sent automatically from the reservation form on the website.',
                'footer2': 'Remember to confirm the reservation!',
                'contact_email': 'Email',
                'contact_phone': 'Phone',
                'lang_pl': 'Polish',
                'lang_en': 'English'
            }
        else:
            labels = {
                'title': 'Nowa rezerwacja',
                'received': 'Otrzymano',
                'name': 'Imię i nazwisko',
                'contact_method': 'Preferowana metoda kontaktu',
                'contact_language': 'Język kontaktu',
                'email': 'Adres e-mail',
                'phone': 'Numer telefonu',
                'service': 'Usługa',
                'additional_info': 'Dodatkowe informacje',
                'footer1': 'Ta rezerwacja została wysłana automatycznie z formularza rezerwacyjnego na stronie internetowej.',
                'footer2': 'Pamiętaj o potwierdzeniu rezerwacji!',
                'contact_email': 'E-mail',
                'contact_phone': 'Telefon',
                'lang_pl': 'Polski',
                'lang_en': 'English'
            }
        
        preferred_contact = labels['contact_email'] if data['contact_method'] == 'email' else labels['contact_phone']
        contact_lang_display = labels['lang_en'] if language == 'en' else labels['lang_pl']
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #e8f5e8; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
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
                    <h2>{labels['title']}</h2>
                    <p>{labels['received']}: {timestamp}</p>
                </div>

                <div class="field highlight">
                    <div class="label">{labels['name']}:</div>
                    <div class="value">{data['name']}</div>
                </div>

                <div class="field">
                    <div class="label">{labels['contact_method']}:</div>
                    <div class="value">{preferred_contact}</div>
                </div>

                <div class="field">
                    <div class="label">{labels['contact_language']}:</div>
                    <div class="value">{contact_lang_display}</div>
                </div>

                <div class="field">
                    <div class="label">{labels['email']}:</div>
                    <div class="value">{data['email']}</div>
                </div>

                {f'<div class="field"><div class="label">{labels["phone"]}:</div><div class="value">{data["phone"]}</div></div>' if data.get('phone') else ''}

                {f'<div class="field"><div class="label">{labels["service"]}:</div><div class="value">{data["service"]}</div></div>' if data.get('service') else ''}

                {f'<div class="field"><div class="label">{labels["additional_info"]}:</div><div class="value">{data["additional_info"].replace(chr(10), "<br>")}</div></div>' if data.get('additional_info') else ''}

                <div class="footer">
                    <p>{labels['footer1']}</p>
                    <p><strong>{labels['footer2']}</strong></p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_reservation_email_text(self, data):
        """Create plain text email body for reservation form"""
        language = data.get('language', 'pl')
        
        # Bilingual field labels
        if language == 'en':
            labels = {
                'title': 'NEW RESERVATION',
                'received': 'Received',
                'name': 'Name',
                'contact_method': 'Preferred contact method',
                'contact_language': 'Contact language',
                'email': 'Email address',
                'phone': 'Phone number',
                'service': 'Service',
                'additional_info': 'Additional information',
                'footer1': 'This reservation was sent automatically from the reservation form on the website.',
                'footer2': 'REMEMBER TO CONFIRM THE RESERVATION!',
                'contact_email': 'Email',
                'contact_phone': 'Phone',
                'lang_pl': 'Polish',
                'lang_en': 'English'
            }
        else:
            labels = {
                'title': 'NOWA REZERWACJA',
                'received': 'Otrzymano',
                'name': 'Imię i nazwisko',
                'contact_method': 'Preferowana metoda kontaktu',
                'contact_language': 'Język kontaktu',
                'email': 'Adres e-mail',
                'phone': 'Numer telefonu',
                'service': 'Usługa',
                'additional_info': 'Dodatkowe informacje',
                'footer1': 'Ta rezerwacja została wysłana automatycznie z formularza rezerwacyjnego na stronie internetowej.',
                'footer2': 'PAMIĘTAJ O POTWIERDZENIU REZERWACJI!',
                'contact_email': 'E-mail',
                'contact_phone': 'Telefon',
                'lang_pl': 'Polski',
                'lang_en': 'English'
            }
        
        preferred_contact = labels['contact_email'] if data['contact_method'] == 'email' else labels['contact_phone']
        contact_lang_display = labels['lang_en'] if language == 'en' else labels['lang_pl']
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        text = f"""
{labels['title']}
{labels['received']}: {timestamp}

{labels['name']}: {data['name']}
{labels['contact_method']}: {preferred_contact}
{labels['contact_language']}: {contact_lang_display}
{labels['email']}: {data['email']}
"""

        if data.get('phone'):
            text += f"{labels['phone']}: {data['phone']}\n"

        if data.get('service'):
            text += f"{labels['service']}: {data['service']}\n"

        if data.get('additional_info'):
            text += f"\n{labels['additional_info']}:\n{data['additional_info']}\n"

        text += f"\n---\n{labels['footer1']}"
        text += f"\n{labels['footer2']}"

        return text