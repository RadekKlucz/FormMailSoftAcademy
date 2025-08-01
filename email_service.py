import os
import smtplib
import logging
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
            msg['Subject'] = f"Nowa wiadomość kontaktowa - {form_data['name']}"
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
            msg['Subject'] = f"Nowa rezerwacja - {form_data['name']}"
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
        preferred_contact = "E-mail" if data['contact_method'] == 'email' else "Telefon"
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
                    <h2>Nowa wiadomość kontaktowa</h2>
                    <p>Otrzymano: {timestamp}</p>
                </div>
                
                <div class="field">
                    <div class="label">Imię i nazwisko:</div>
                    <div class="value">{data['name']}</div>
                </div>
                
                <div class="field">
                    <div class="label">Preferowana metoda kontaktu:</div>
                    <div class="value">{preferred_contact}</div>
                </div>
                
                <div class="field">
                    <div class="label">Adres e-mail:</div>
                    <div class="value">{data['email']}</div>
                </div>
                
                {f'<div class="field"><div class="label">Numer telefonu:</div><div class="value">{data["phone"]}</div></div>' if data.get('phone') else ''}
                
                {f'<div class="field"><div class="label">Wiadomość:</div><div class="value">{data["message"].replace(chr(10), "<br>")}</div></div>' if data.get('message') else ''}
                
                <div class="footer">
                    <p>Ta wiadomość została wysłana automatycznie z formularza kontaktowego na stronie internetowej.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_contact_email_text(self, data):
        """Create plain text email body for contact form"""
        preferred_contact = "E-mail" if data['contact_method'] == 'email' else "Telefon"
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        text = f"""
NOWA WIADOMOŚĆ KONTAKTOWA
Otrzymano: {timestamp}

Imię i nazwisko: {data['name']}
Preferowana metoda kontaktu: {preferred_contact}
Adres e-mail: {data['email']}
"""
        
        if data.get('phone'):
            text += f"Numer telefonu: {data['phone']}\n"
        
        if data.get('message'):
            text += f"\nWiadomość:\n{data['message']}\n"
        
        text += "\n---\nTa wiadomość została wysłana automatycznie z formularza kontaktowego na stronie internetowej."
        
        return text
    
    def _create_reservation_email_html(self, data):
        """Create HTML email body for reservation form"""
        preferred_contact = "E-mail" if data['contact_method'] == 'email' else "Telefon"
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
                    <h2>Nowa rezerwacja</h2>
                    <p>Otrzymano: {timestamp}</p>
                </div>
                
                <div class="field highlight">
                    <div class="label">Imię i nazwisko:</div>
                    <div class="value">{data['name']}</div>
                </div>
                
                <div class="field">
                    <div class="label">Preferowana metoda kontaktu:</div>
                    <div class="value">{preferred_contact}</div>
                </div>
                
                <div class="field">
                    <div class="label">Adres e-mail:</div>
                    <div class="value">{data['email']}</div>
                </div>
                
                {f'<div class="field"><div class="label">Numer telefonu:</div><div class="value">{data["phone"]}</div></div>' if data.get('phone') else ''}
                
                {f'<div class="field"><div class="label">Usługa:</div><div class="value">{data["service"]}</div></div>' if data.get('service') else ''}
                
                {f'<div class="field"><div class="label">Dodatkowe informacje:</div><div class="value">{data["additional_info"].replace(chr(10), "<br>")}</div></div>' if data.get('additional_info') else ''}
                
                <div class="footer">
                    <p>Ta rezerwacja została wysłana automatycznie z formularza rezerwacyjnego na stronie internetowej.</p>
                    <p><strong>Pamiętaj o potwierdzeniu rezerwacji!</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_reservation_email_text(self, data):
        """Create plain text email body for reservation form"""
        preferred_contact = "E-mail" if data['contact_method'] == 'email' else "Telefon"
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        text = f"""
NOWA REZERWACJA
Otrzymano: {timestamp}

Imię i nazwisko: {data['name']}
Preferowana metoda kontaktu: {preferred_contact}
Adres e-mail: {data['email']}
"""
        
        if data.get('phone'):
            text += f"Numer telefonu: {data['phone']}\n"
        
        if data.get('service'):
            text += f"Usługa: {data['service']}\n"
        
        if data.get('additional_info'):
            text += f"\nDodatkowe informacje:\n{data['additional_info']}\n"
        
        text += "\n---\nTa rezerwacja została wysłana automatycznie z formularza rezerwacyjnego na stronie internetowej."
        text += "\nPAMIĘTAJ O POTWIERDZENIU REZERWACJI!"
        
        return text
