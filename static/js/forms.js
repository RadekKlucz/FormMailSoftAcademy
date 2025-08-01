// Form submission handlers and utilities

// Show status message
function showStatus(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 'alert-info';
    
    element.innerHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}

// Submit form data to API
async function submitForm(endpoint, formData, statusElementId) {
    try {
        showStatus(statusElementId, 'Wysyłanie...', 'info');
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(statusElementId, data.message || 'Formularz został wysłany pomyślnie!', 'success');
            return true;
        } else {
            const errorMessage = Array.isArray(data.error) ? data.error.join(', ') : data.error;
            showStatus(statusElementId, `Błąd: ${errorMessage}`, 'error');
            return false;
        }
    } catch (error) {
        console.error('Network error:', error);
        showStatus(statusElementId, 'Błąd sieci. Sprawdź połączenie internetowe.', 'error');
        return false;
    }
}

// Contact form handler
document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('contactName').value.trim(),
        email: document.getElementById('contactEmailAddr').value.trim(),
        contact_method: document.querySelector('input[name="contactMethod"]:checked').value,
        phone: document.getElementById('contactPhoneNum').value.trim(),
        message: document.getElementById('contactMessage').value.trim()
    };
    
    // Client-side validation
    if (!formData.name || formData.name.length < 2) {
        showStatus('contactStatus', 'Imię jest wymagane (minimum 2 znaki)', 'error');
        return;
    }
    
    if (!formData.email) {
        showStatus('contactStatus', 'Adres e-mail jest wymagany', 'error');
        return;
    }
    
    if (formData.contact_method === 'phone' && !formData.phone) {
        showStatus('contactStatus', 'Numer telefonu jest wymagany gdy wybrano kontakt telefoniczny', 'error');
        return;
    }
    
    const success = await submitForm('/api/contact', formData, 'contactStatus');
    
    if (success) {
        // Reset form on success
        document.getElementById('contactForm').reset();
        document.getElementById('contactEmail').checked = true;
    }
});

// Reservation form handler
document.getElementById('reservationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('reservationName').value.trim(),
        email: document.getElementById('reservationEmailAddr').value.trim(),
        contact_method: document.querySelector('input[name="reservationContactMethod"]:checked').value,
        phone: document.getElementById('reservationPhoneNum').value.trim(),
        service: document.getElementById('reservationService').value,
        additional_info: document.getElementById('reservationInfo').value.trim()
    };
    
    // Client-side validation
    if (!formData.name || formData.name.length < 2) {
        showStatus('reservationStatus', 'Imię jest wymagane (minimum 2 znaki)', 'error');
        return;
    }
    
    if (!formData.email) {
        showStatus('reservationStatus', 'Adres e-mail jest wymagany', 'error');
        return;
    }
    
    if (formData.contact_method === 'phone' && !formData.phone) {
        showStatus('reservationStatus', 'Numer telefonu jest wymagany gdy wybrano kontakt telefoniczny', 'error');
        return;
    }
    
    const success = await submitForm('/api/reservation', formData, 'reservationStatus');
    
    if (success) {
        // Reset form on success
        document.getElementById('reservationForm').reset();
        document.getElementById('reservationEmail').checked = true;
    }
});

// API health check
async function checkApiHealth() {
    try {
        showStatus('apiStatus', 'Sprawdzanie stanu API...', 'info');
        
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (response.ok) {
            const emailStatus = data.email_service ? 'Połączony' : 'Błąd połączenia';
            const emailClass = data.email_service ? 'text-success' : 'text-danger';
            
            document.getElementById('apiStatus').innerHTML = `
                <div class="alert alert-success">
                    <h5><i class="fas fa-check-circle me-2"></i>API Status: ${data.status}</h5>
                    <p><strong>Czas:</strong> ${new Date(data.timestamp).toLocaleString('pl-PL')}</p>
                    <p><strong>Serwis email:</strong> <span class="${emailClass}">${emailStatus}</span></p>
                </div>
            `;
        } else {
            showStatus('apiStatus', 'Błąd podczas sprawdzania statusu API', 'error');
        }
    } catch (error) {
        console.error('Health check error:', error);
        showStatus('apiStatus', 'Błąd sieci podczas sprawdzania statusu', 'error');
    }
}

// Form field validation helpers
document.addEventListener('DOMContentLoaded', function() {
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (this.value && !emailPattern.test(this.value)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
    
    // Phone validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const phonePattern = /^(\+48\s?)?[\d\s\-\(\)]{7,15}$/;
            if (this.value && !phonePattern.test(this.value)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
    
    // Name validation
    const nameInputs = document.querySelectorAll('input[id$="Name"]');
    nameInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && this.value.trim().length < 2) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
    
    // Dynamic phone field requirement based on contact method
    const contactMethodRadios = document.querySelectorAll('input[type="radio"][name*="contactMethod"], input[type="radio"][name*="ContactMethod"]');
    contactMethodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const formPrefix = this.name.includes('reservation') ? 'reservation' : 'contact';
            const phoneField = document.getElementById(formPrefix + 'PhoneNum');
            
            if (this.value === 'phone') {
                phoneField.required = true;
                phoneField.parentElement.querySelector('.form-text').textContent = 'Wymagane dla wybranej metody kontaktu';
            } else {
                phoneField.required = false;
                phoneField.parentElement.querySelector('.form-text').textContent = 'Opcjonalne';
            }
        });
    });
});

// Auto-check API health on page load
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(checkApiHealth, 1000);
});
