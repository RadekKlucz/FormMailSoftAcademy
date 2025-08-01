#!/usr/bin/env python3
"""
Skrypt do uruchomienia aplikacji lokalnie z automatycznym ładowaniem .env
"""
import os
import sys
from pathlib import Path

def load_env_file():
    """Ładuje zmienne z pliku .env"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Brak pliku .env!")
        print("Stwórz plik .env z zawartością:")
        print("""
GMAIL_EMAIL=twoja-firma@gmail.com
GMAIL_APP_PASSWORD=twoje-haslo-aplikacji
RECIPIENT_EMAIL=kontakt@twoja-firma.com
SESSION_SECRET=wygenerowany-losowy-klucz
        """)
        return False
    
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value
    
    return True

def check_requirements():
    """Sprawdza czy wszystkie wymagane pakiety są zainstalowane"""
    required_packages = [
        'flask', 'flask_cors', 'flask_limiter', 
        'email_validator', 'werkzeug'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Brakujące pakiety:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nZainstaluj komendą:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    print("🚀 Uruchamianie aplikacji API Formularzy...")
    
    # Sprawdź wymagania
    if not check_requirements():
        sys.exit(1)
    
    # Załaduj zmienne środowiskowe
    if not load_env_file():
        sys.exit(1)
    
    print("✅ Zmienne środowiskowe załadowane")
    print("✅ Wszystkie pakiety dostępne")
    
    # Uruchom aplikację
    try:
        from main import app
        print("🌐 Aplikacja uruchomiona na: http://localhost:5000")
        print("📧 Testuj formularze na: http://localhost:5000")
        print("🔍 Status API: http://localhost:5000/api/health")
        print("\n💡 Naciśnij Ctrl+C aby zatrzymać serwer")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\n👋 Serwer zatrzymany")
    except Exception as e:
        print(f"❌ Błąd uruchomienia: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())