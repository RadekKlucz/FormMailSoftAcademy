# 📧 Szybka Konfiguracja - API Formularzy

## 🎯 Co musisz zrobić (5 kroków)

### 1️⃣ Przygotuj konto Gmail

1. Przejdź do **https://myaccount.google.com/security**
2. Włącz **"Uwierzytelnianie dwuetapowe"** (jeśli nie masz)
3. Kliknij **"Hasła aplikacji"**
4. Wybierz **"Mail"** → **"Inne"** → wpisz "API Formularzy"
5. **Skopiuj 16-znakowy kod** (to jest GMAIL_APP_PASSWORD)

### 2️⃣ Wybierz platformę hostingową

**Polecane dla backendu:**
- ✅ **Vercel** - najłatwiejszy setup dla Flask
- ✅ **Railway** - dobry dla początkujących  
- ✅ **Render** - darmowy tier dostępny

### 3️⃣ Ustaw zmienne środowiskowe

W swojej platformie hostingowej dodaj:

```
GMAIL_EMAIL=twoja-firma@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop  
RECIPIENT_EMAIL=kontakt@twoja-firma.com
SESSION_SECRET=wygenerowany-losowy-klucz-64-znaki
API_SECRET_KEY=wygenerowany-api-klucz-64-znaki
```

**Generowanie kluczy:**
```bash
# SESSION_SECRET
python -c "import secrets; print(secrets.token_hex(32))"

# API_SECRET_KEY (opcjonalne - dla dodatkowych zabezpieczeń)
python -c "import secrets; print(secrets.token_hex(32))"
```

**Generowanie SESSION_SECRET:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4️⃣ Wgraj kod

1. Skopiuj wszystkie pliki z tego projektu
2. Użyj pliku `requirements-production.txt` jako `requirements.txt`
3. Deploy na wybranej platformie

### 5️⃣ Przetestuj

Sprawdź endpoint:
```
https://twoj-backend.vercel.app/api/health
```

Powinna zwrócić: `"email_service": true`

---

## 🌐 Integracja z Frontend (Netlify)

W swoim kodzie JavaScript na Netlify:

```javascript
// Zmień URL na swój backend
const API_URL = 'https://twoj-backend.vercel.app';

const response = await fetch(`${API_URL}/api/contact`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "Jan Kowalski",
    contact_method: "email", // lub "phone"
    email: "jan@example.com",
    message: "Treść wiadomości"
  })
});
```

---

## 🚨 Częste Problemy

**Problem**: `email_service: false`
**Rozwiązanie**: Sprawdź GMAIL_EMAIL i GMAIL_APP_PASSWORD

**Problem**: CORS error  
**Rozwiązanie**: Dodaj domenę frontend w app.py:
```python
CORS(app, origins=["https://twoja-strona.netlify.app"])
```

**Problem**: 535 Authentication error
**Rozwiązanie**: Upewnij się, że używasz hasła aplikacji, nie zwykłego hasła

---

## 📞 Gdzie znajdziesz pomoc

1. **DEPLOYMENT.md** - szczegółowe instrukcje
2. **frontend-example.html** - przykład formularza
3. **vercel.json** - gotowa konfiguracja Vercel