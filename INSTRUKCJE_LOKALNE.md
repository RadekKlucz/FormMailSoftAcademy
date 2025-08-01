# 🏠 Uruchomienie na Własnym Komputerze

## Wymagania
- Python 3.8+ zainstalowany na komputerze
- Dostęp do internetu (do wysyłania emaili)

## Kroki instalacji

### 1️⃣ Pobierz projekt
```bash
# Skopiuj wszystkie pliki z tego projektu do folderu na swoim komputerze
# np. C:\moj-projekt\ lub ~/moj-projekt/
```

### 2️⃣ Zainstaluj zależności
```bash
# Przejdź do folderu projektu w terminalu/cmd
cd moj-projekt

# Zainstaluj potrzebne pakiety
pip install Flask Flask-CORS Flask-Limiter email-validator gunicorn Werkzeug
```

### 3️⃣ Utwórz plik .env
Stwórz plik `.env` w głównym folderze projektu:

```env
# Plik .env - NIE UDOSTĘPNIAJ NIKOMU!
GMAIL_EMAIL=twoja-firma@gmail.com
GMAIL_APP_PASSWORD=qvve mmcs ndue yyff
RECIPIENT_EMAIL=kontakt@twoja-firma.com
SESSION_SECRET=wygenerowany-losowy-klucz-64-znaki
```

**Jak wygenerować SESSION_SECRET:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4️⃣ Uruchom aplikację
```bash
# Sposób 1: Bezpośrednio przez Flask (do testowania)
python -m flask --app main run --host=0.0.0.0 --port=5000 --debug

# Sposób 2: Przez gunicorn (jak w produkcji)
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### 5️⃣ Testuj aplikację
Otwórz przeglądarkę i idź na:
- **http://localhost:5000** - strona testowa z formularzami
- **http://localhost:5000/api/health** - sprawdź czy działa

## 🔧 Rozwiązywanie problemów

**Problem**: `ModuleNotFoundError`
```bash
# Zainstaluj brakujący moduł
pip install nazwa-modulu
```

**Problem**: Port 5000 zajęty
```bash
# Użyj innego portu
python -m flask --app main run --port=8000
```

**Problem**: Błąd Gmail 535
- Sprawdź czy GMAIL_APP_PASSWORD to hasło aplikacji (nie zwykłe hasło)
- Sprawdź czy uwierzytelnianie dwuetapowe jest włączone

## 📁 Struktura plików
```
moj-projekt/
├── .env              # Twoje sekrety (STWÓRZ TO!)
├── main.py           # Główny plik aplikacji
├── app.py            # Konfiguracja Flask
├── email_service.py  # Obsługa emaili
├── validators.py     # Walidacja formularzy
├── templates/        # Szablony HTML
└── static/          # CSS/JS
```

## 🚀 Gotowe do testowania!
Po uruchomieniu możesz:
1. Wypełnić formularz na http://localhost:5000
2. Sprawdzić czy email dotarł na RECIPIENT_EMAIL
3. Testować różne scenariusze (błędne dane, puste pola)