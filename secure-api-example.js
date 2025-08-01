/**
 * Przykład prostego klienta API z autentykacją
 * SUPER ŁATWE W IMPLEMENTACJI!
 */

class SimpleSecureAPIClient {
    constructor(apiUrl, apiKey = null) {
        this.apiUrl = apiUrl;
        this.apiKey = apiKey;
    }

    // Wysyła zabezpieczone żądanie z prostym API key
    async sendRequest(endpoint, data) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };

            // Jeśli masz API key, dodaj go do headers
            if (this.apiKey) {
                headers['X-API-Key'] = this.apiKey;
            }

            const response = await fetch(`${this.apiUrl}${endpoint}`, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Wysyła formularz kontaktowy
    async sendContactForm(formData) {
        return this.sendRequest('/api/contact', formData);
    }

    // Wysyła formularz rezerwacji
    async sendReservationForm(formData) {
        return this.sendRequest('/api/reservation', formData);
    }

    // Sprawdza czy API wymaga autentykacji
    async checkAuthRequirements() {
        try {
            const response = await fetch(`${this.apiUrl}/api/auth-info`);
            return await response.json();
        } catch (error) {
            console.error('Auth check failed:', error);
            return { authentication_required: false };
        }
    }
}

// Przykład użycia:
/*
// 1. Inicjalizacja klienta
const apiClient = new SecureAPIClient(
    'https://twoja-app.vercel.app',
    'twoj-wygenerowany-api-key'
);

// 2. Wysłanie formularza kontaktowego
document.getElementById('contactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        contact_method: 'email',
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };

    try {
        const response = await apiClient.sendContactForm(formData);
        console.log('Success:', response);
        alert('Wiadomość wysłana pomyślnie!');
    } catch (error) {
        console.error('Error:', error);
        alert('Błąd wysyłania: ' + error.message);
    }
});
*/

// Alternatywnie - prostsze API bez podpisu (mniej bezpieczne)
class SimpleAPIClient {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
    }

    async sendRequest(endpoint, data) {
        const response = await fetch(`${this.apiUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Request failed');
        }

        return await response.json();
    }

    async sendContactForm(formData) {
        return this.sendRequest('/api/contact', formData);
    }
}