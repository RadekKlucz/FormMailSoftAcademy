/**
 * Przykład bezpiecznego klienta API z autentykacją HMAC
 * Użyj tego kodu w swoim frontend jeśli chcesz dodać zabezpieczenia
 */

class SecureAPIClient {
    constructor(apiUrl, apiKey) {
        this.apiUrl = apiUrl;
        this.apiKey = apiKey;
    }

    // Generuje podpis HMAC dla danych
    async generateSignature(data) {
        const encoder = new TextEncoder();
        const dataString = JSON.stringify(data);
        const keyData = encoder.encode(this.apiKey);
        const messageData = encoder.encode(dataString);

        const cryptoKey = await crypto.subtle.importKey(
            'raw',
            keyData,
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
        );

        const signature = await crypto.subtle.sign('HMAC', cryptoKey, messageData);
        return Array.from(new Uint8Array(signature))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    // Wysyła zabezpieczone żądanie do API
    async sendSecureRequest(endpoint, data) {
        try {
            const signature = await this.generateSignature(data);
            
            const response = await fetch(`${this.apiUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': this.apiKey,
                    'X-Signature': signature
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Secure API request failed:', error);
            throw error;
        }
    }

    // Wysyła formularz kontaktowy (zabezpieczony)
    async sendContactForm(formData) {
        return this.sendSecureRequest('/api/contact', formData);
    }

    // Wysyła formularz rezerwacji (zabezpieczony)
    async sendReservationForm(formData) {
        return this.sendSecureRequest('/api/reservation', formData);
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