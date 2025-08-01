# 📦 Pliki do Deploymentu na Hostingu

## ✅ WYMAGANE pliki do deploymentu

### Kod aplikacji (NIEZBĘDNE)
- **`main.py`** - główny plik aplikacji (entry point)
- **`app.py`** - konfiguracja Flask 
- **`email_service.py`** - obsługa wysyłania emaili
- **`validators.py`** - walidacja formularzy
- **`templates/`** - folder z szablonami HTML
  - `templates/index.html`
  - `templates/test_forms.html`
- **`static/`** - folder z plikami CSS/JS (jeśli istnieje)

### Konfiguracja hostingu
- **`requirements-production.txt`** - zależności Python (skopiuj jako `requirements.txt`)
- **`runtime.txt`** - wersja Python
- **`vercel.json`** - konfiguracja dla Vercel

## ❌ NIEPOTRZEBNE pliki (można usunąć)

### Dokumentacja i instrukcje (USUŃ)
- **`DEPLOYMENT.md`** - instrukcje deployment (tylko dla Ciebie)
- **`INSTRUKCJE_LOKALNE.md`** - instrukcje uruchomienia lokalnego
- **`KONFIGURACJA.md`** - przewodnik konfiguracji
- **`replit.md`** - dokumentacja projektu Replit
- **`PLIKI_DEPLOYMENT.md`** - ten plik

### Pliki lokalne (USUŃ)
- **`run_local.py`** - skrypt do uruchomienia lokalnego
- **`frontend-example.html`** - przykład integracji
- **`.env.example`** - przykład zmiennych środowiskowych

### Pliki Replit (USUŃ)
- **`pyproject.toml`** - konfiguracja Replit
- **`uv.lock`** - lock file Replit
- **`__pycache__/`** - folder cache Python
- **`attached_assets/`** - załączone obrazy

### Pliki tymczasowe (USUŃ)
- Wszystkie pliki `.pyc`
- Foldery `__pycache__`
- Pliki `.env` (jeśli istnieją) - NIGDY nie przesyłaj!

## 📋 Minimalna struktura do deploymentu

```
twoj-projekt/
├── main.py              # ✅ WYMAGANE
├── app.py               # ✅ WYMAGANE  
├── email_service.py     # ✅ WYMAGANE
├── validators.py        # ✅ WYMAGANE
├── requirements.txt     # ✅ WYMAGANE (skopiuj z requirements-production.txt)
├── runtime.txt          # ✅ WYMAGANE
├── vercel.json          # ✅ WYMAGANE (dla Vercel)
├── templates/           # ✅ WYMAGANE
│   ├── index.html
│   └── test_forms.html
└── static/              # ✅ WYMAGANE (jeśli istnieje)
    └── js/
```

## 🚀 Kroki przed deploymentem

1. **Skopiuj tylko wymagane pliki** do nowego folderu
2. **Zmień nazwę** `requirements-production.txt` → `requirements.txt`
3. **Ustaw zmienne środowiskowe** na platformie hostingowej
4. **Deploy!**

## ⚠️ UWAGA - Nigdy nie przesyłaj:
- Plików `.env` z rzeczywistymi hasłami
- Folderów `__pycache__` 
- Dokumentacji markdown (.md)
- Plików przykładowych i testowych