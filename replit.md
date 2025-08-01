# API Formularzy - Flask Contact Form Service

## Overview

A Flask-based web service that provides a contact form API with email functionality. The application handles form submissions through a REST API, validates input data, and sends formatted emails using Gmail SMTP. It includes a web interface for testing forms and comprehensive rate limiting for security.

## User Preferences

Preferred communication style: Simple, everyday language.
Deployment target: Netlify for frontend, separate backend hosting (Vercel/Railway recommended)
Configuration approach: Environment variables with detailed setup instructions

## System Architecture

### Backend Framework
- **Flask** as the primary web framework with WSGI deployment capability
- **CORS enabled** for cross-origin requests with configurable origins
- **ProxyFix middleware** for handling reverse proxy headers

### API Design
- RESTful endpoints with JSON request/response format
- Rate limiting implemented at multiple levels:
  - Global: 100 requests per hour per IP
  - Contact form: 5 submissions per minute per IP
- Centralized error handling and validation

### Email System
- **Gmail SMTP integration** for reliable email delivery
- HTML and plain text email formats for better compatibility
- Configurable sender/recipient addresses via environment variables
- Connection testing capability for diagnostics

### Input Validation & Security
- **Custom validation layer** with sanitization for XSS prevention
- Form-specific validators for contact and reservation forms with Polish localization
- Conditional field validation: email OR phone required based on contact method preference
- Email format validation with RFC compliance
- Phone number validation for Polish formats
- HTML entity encoding for safe output
- Ensures at least one contact method is always provided

### Frontend Components
- **Bootstrap-based UI** with dark theme support
- Responsive design for mobile compatibility
- Interactive form testing interface
- Real-time status feedback with error handling
- Font Awesome icons for enhanced UX

### Configuration Management
- Environment variable based configuration
- Separate development and production settings
- Configurable SMTP credentials and recipient addresses
- Session secret management

## External Dependencies

### Core Framework Dependencies
- **Flask** - Web application framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Limiter** - Rate limiting functionality
- **Werkzeug** - WSGI utilities and middleware

### Email Services
- **Gmail SMTP** - Email delivery service requiring app-specific passwords
- **Python smtplib** - Built-in SMTP client library

### Frontend Libraries
- **Bootstrap 5** - UI framework with dark theme
- **Font Awesome 6** - Icon library
- **Vanilla JavaScript** - Client-side form handling

### Environment Variables Required
- `GMAIL_EMAIL` - Sender email address
- `GMAIL_APP_PASSWORD` - Gmail app-specific password
- `RECIPIENT_EMAIL` - Default recipient for form submissions
- `SESSION_SECRET` - Flask session encryption key