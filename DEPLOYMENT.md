# Instrukcje Wdrożenia - API Formularzy

## Konfiguracja dla Netlify Functions lub Vercel

Ponieważ Netlify jest przeznaczony głównie dla frontend'u, do hostowania tego backendu API masz kilka opcji:

### Opcja 1: Netlify Functions (Serverless)
1. Przenieś logikę backendu do funkcji Netlify
2. Utwórz folder `netlify/functions/`
3. Każdy endpoint jako osobna funkcja

### Opcja 2: Vercel (Zalecane dla Flask)
1. Dodaj plik `vercel.json` (już stworzony)
2. Deploy na Vercel, który lepiej obsługuje Python

### Opcja 3: Railway/Render/Heroku
Platformy dedykowane dla backendu z bazami danych

## Zmienne Środowiskowe do Skonfigurowania

Bez względu na wybraną platformę, musisz ustawić te zmienne:

### 1. GMAIL_EMAIL
- **Opis**: Adres Gmail, z którego będą wysyłane wiadomości
- **Przykład**: `kontakt@twoja-firma.com` lub `twoja-firma@gmail.com`
- **Instrukcje**:
  1. Utwórz konto Gmail dedykowane dla firmy (opcjonalne)
  2. Skopiuj pełny adres email

### 2. GMAIL_APP_PASSWORD
- **Opis**: Hasło aplikacji Gmail (NIE zwykłe hasło konta!)
- **Instrukcje krok po kroku**:
  1. Przejdź do https://myaccount.google.com/security
  2. W sekcji "Logowanie w Google" upewnij się, że masz włączone "Uwierzytelnianie dwuetapowe"
  3. Kliknij "Hasła aplikacji" (App Passwords)
  4. Wybierz "Mail" jako aplikację
  5. Wybierz "Inne" jako urządzenie i wpisz "API Formularzy"
  6. Skopiuj wygenerowany 16-znakowy kod (bez spacji)
  7. **To jest Twoje GMAIL_APP_PASSWORD**

### 3. RECIPIENT_EMAIL
- **Opis**: Adres, na który będą przychodzić wszystkie formularze
- **Przykład**: `zamowienia@twoja-firma.com` lub `info@twoja-firma.com`
- **Uwaga**: Może być taki sam jak GMAIL_EMAIL

### 4. SESSION_SECRET
- **Opis**: Losowy klucz do szyfrowania sesji
- **Generowanie**:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- **Przykład**: `a1b2c3d4e5f6...` (64 znaki)

## Konfiguracja w różnych serwisach

### Vercel
1. Przejdź do Settings → Environment Variables
2. Dodaj każdą zmienną osobno

### Netlify
1. Site settings → Environment variables
2. Dodaj każdą zmienną osobno

### Railway/Render
1. Variables lub Environment tabs
2. Dodaj zmienne

## Testowanie Konfiguracji

Po wdrożeniu, sprawdź endpoint:
```
GET https://twoja-domena.com/api/health
```

Powinna zwrócić:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "email_service": true
}
```

Jeśli `email_service: false`, sprawdź zmienne środowiskowe.

## Bezpieczeństwo CORS

W produkcji zmień w `app.py`:
```python
CORS(app, origins=["https://twoja-strona.netlify.app"])
```

## Struktura Projektu dla Frontend

Twój frontend na Netlify powinien wysyłać żądania POST do:
- `https://twoj-backend.vercel.app/api/contact`
- `https://twoj-backend.vercel.app/api/reservation`

Przykład JavaScript:
```javascript
const response = await fetch('https://twoj-backend.vercel.app/api/contact', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});
```