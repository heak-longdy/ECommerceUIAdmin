// Payment Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializePayment();
});

function initializePayment() {
    setupPaymentMethods();
    setupCardValidation();
    setupFormAnimations();
    loadSavedData();
}

// Payment Method Selection
function setupPaymentMethods() {
    const paymentMethods = document.querySelectorAll('input[name="payment-method"]');
    
    paymentMethods.forEach(method => {
        method.addEventListener('change', switchPaymentMethod);
    });
}

function switchPaymentMethod() {
    const selectedMethod = document.querySelector('input[name="payment-method"]:checked').value;
    
    // Hide all payment forms
    document.querySelectorAll('.payment-form').forEach(form => {
        form.classList.add('hidden');
    });
    
    // Show selected payment form
    const selectedForm = document.getElementById(`${selectedMethod}-form`);
    if (selectedForm) {
        selectedForm.classList.remove('hidden');
        selectedForm.classList.add('fade-in');
    }
}

// Card Validation
function setupCardValidation() {
    const cardNumber = document.getElementById('card-number');
    const expiryDate = document.getElementById('expiry-date');
    const cvv = document.getElementById('cvv');
    const cardholderName = document.getElementById('cardholder-name');
    
    if (cardNumber) {
        cardNumber.addEventListener('input', handleCardNumberInput);
        cardNumber.addEventListener('blur', validateCardNumber);
    }
    
    if (expiryDate) {
        expiryDate.addEventListener('input', handleExpiryInput);
        expiryDate.addEventListener('blur', validateExpiryDate);
    }
    
    if (cvv) {
        cvv.addEventListener('input', handleCVVInput);
        cvv.addEventListener('blur', validateCVV);
    }
    
    if (cardholderName) {
        cardholderName.addEventListener('blur', validateCardholderName);
    }
}

function handleCardNumberInput(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    // Add spaces every 4 digits
    value = value.replace(/(\d{4})(?=\d)/g, '$1 ');
    
    e.target.value = value;
    
    // Detect card brand
    updateCardBrand(value);
    
    // Real-time validation
    if (value.replace(/\s/g, '').length >= 13) {
        validateCardNumber({ target: e.target });
    }
}

function updateCardBrand(cardNumber) {
    const cleanNumber = cardNumber.replace(/\s/g, '');
    const brandIcon = document.querySelector('.card-brand-icon');
    
    if (!brandIcon) return;
    
    brandIcon.className = 'card-brand-icon';
    
    if (/^4/.test(cleanNumber)) {
        brandIcon.classList.add('visa');
    } else if (/^5[1-5]|^2[2-7]/.test(cleanNumber)) {
        brandIcon.classList.add('mastercard');
    } else if (/^3[47]/.test(cleanNumber)) {
        brandIcon.classList.add('amex');
    } else if (/^6(?:011|5)/.test(cleanNumber)) {
        brandIcon.classList.add('discover');
    }
}

function validateCardNumber(e) {
    const cardNumber = e.target.value.replace(/\s/g, '');
    const field = e.target;
    
    clearFieldError(field);
    
    if (!cardNumber) {
        showFieldError(field, 'Card number is required');
        return false;
    }
    
    if (!isValidCardNumber(cardNumber)) {
        showFieldError(field, 'Please enter a valid card number');
        return false;
    }
    
    field.classList.add('valid');
    return true;
}

function isValidCardNumber(cardNumber) {
    // Luhn algorithm implementation
    let sum = 0;
    let isEven = false;
    
    for (let i = cardNumber.length - 1; i >= 0; i--) {
        let digit = parseInt(cardNumber.charAt(i));
        
        if (isEven) {
            digit *= 2;
            if (digit > 9) {
                digit -= 9;
            }
        }
        
        sum += digit;
        isEven = !isEven;
    }
    
    return sum % 10 === 0 && cardNumber.length >= 13 && cardNumber.length <= 19;
}

function handleExpiryInput(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    
    e.target.value = value;
    
    if (value.length === 5) {
        validateExpiryDate({ target: e.target });
    }
}

function validateExpiryDate(e) {
    const expiry = e.target.value;
    const field = e.target;
    
    clearFieldError(field);
    
    if (!expiry) {
        showFieldError(field, 'Expiry date is required');
        return false;
    }
    
    const [month, year] = expiry.split('/');
    
    if (!month || !year || month.length !== 2 || year.length !== 2) {
        showFieldError(field, 'Please enter a valid expiry date (MM/YY)');
        return false;
    }
    
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear() % 100;
    const currentMonth = currentDate.getMonth() + 1;
    
    const expMonth = parseInt(month);
    const expYear = parseInt(year);
    
    if (expMonth < 1 || expMonth > 12) {
        showFieldError(field, 'Please enter a valid month (01-12)');
        return false;
    }
    
    if (expYear < currentYear || (expYear === currentYear && expMonth < currentMonth)) {
        showFieldError(field, 'Card has expired');
        return false;
    }
    
    field.classList.add('valid');
    return true;
}

function handleCVVInput(e) {
    e.target.value = e.target.value.replace(/\D/g, '');
}

function validateCVV(e) {
    const cvv = e.target.value;
    const field = e.target;
    
    clearFieldError(field);
    
    if (!cvv) {
        showFieldError(field, 'CVV is required');
        return false;
    }
    
    if (cvv.length < 3 || cvv.length > 4) {
        showFieldError(field, 'Please enter a valid CVV');
        return false;
    }
    
    field.classList.add('valid');
    return true;
}

function validateCardholderName(e) {
    const name = e.target.value.trim();
    const field = e.target;
    
    clearFieldError(field);
    
    if (!name) {
        showFieldError(field, 'Cardholder name is required');
        return false;
    }
    
    if (name.length < 2) {
        showFieldError(field, 'Please enter a valid name');
        return false;
    }
    
    field.classList.add('valid');
    return true;
}

// Form Validation Helpers
function clearFieldError(field) {
    field.classList.remove('error');
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
}

function showFieldError(field, message) {
    field.classList.remove('valid');
    field.classList.add('error');
    
    const errorElement = document.createElement('span');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    
    field.parentNode.appendChild(errorElement);
}

// Animation Setup
function setupFormAnimations() {
    const paymentSection = document.querySelector('.payment-section');
    const orderSummary = document.querySelector('.order-summary');
    
    if (paymentSection) {
        paymentSection.classList.add('fade-in');
    }
    
    if (orderSummary) {
        orderSummary.style.animationDelay = '0.2s';
        orderSummary.classList.add('fade-in');
    }
}

// Load Saved Data
function loadSavedData() {
    const savedCheckoutData = localStorage.getItem('checkoutFormData');
    if (savedCheckoutData) {
        try {
            const data = JSON.parse(savedCheckoutData);
            populateShippingInfo(data);
        } catch (error) {
            console.error('Error loading checkout data:', error);
        }
    }
}

function populateShippingInfo(data) {
    const addressElement = document.querySelector('.address-details');
    if (addressElement && data['first-name'] && data['last-name']) {
        const fullName = `${data['first-name']} ${data['last-name']}`;
        const address = data['address'] || '';
        const apartment = data['apartment'] ? `, ${data['apartment']}` : '';
        const city = data['city'] || '';
        const state = data['state'] || '';
        const zip = data['zip'] || '';
        
        addressElement.innerHTML = `
            <p><strong>${fullName}</strong></p>
            <p>${address}${apartment}</p>
            <p>${city}, ${state} ${zip}</p>
            <p>United States</p>
        `;
    }
}

// Payment Processing
function processPayment() {
    const selectedMethod = document.querySelector('input[name="payment-method"]:checked').value;
    const termsAccepted = document.getElementById('accept-terms').checked;
    
    if (!termsAccepted) {
        showError('Please accept the terms and conditions to continue.');
        return;
    }
    
    if (selectedMethod === 'credit-card') {
        if (!validateCreditCardForm()) {
            return;
        }
    }
    
    // Show processing modal
    showProcessingModal();
    
    // Simulate payment processing
    setTimeout(() => {
        // Clear all saved data
        localStorage.removeItem('checkoutFormData');
        
        // Redirect to confirmation page
        window.location.href = 'order-confirmation.html';
    }, 3000);
}

function validateCreditCardForm() {
    const cardNumber = document.getElementById('card-number');
    const expiryDate = document.getElementById('expiry-date');
    const cvv = document.getElementById('cvv');
    const cardholderName = document.getElementById('cardholder-name');
    
    let isValid = true;
    
    if (!validateCardNumber({ target: cardNumber })) isValid = false;
    if (!validateExpiryDate({ target: expiryDate })) isValid = false;
    if (!validateCVV({ target: cvv })) isValid = false;
    if (!validateCardholderName({ target: cardholderName })) isValid = false;
    
    if (!isValid) {
        showError('Please correct the errors in your payment information.');
        // Scroll to first error
        const firstError = document.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    return isValid;
}

function showProcessingModal() {
    const modal = document.getElementById('processing-modal');
    modal.style.display = 'block';
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function hideProcessingModal() {
    const modal = document.getElementById('processing-modal');
    modal.style.display = 'none';
    
    // Restore body scroll
    document.body.style.overflow = '';
}

function showError(message) {
    // Remove existing error
    const existingError = document.querySelector('.payment-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'payment-error';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
    `;
    
    // Insert at top of payment section
    const paymentSection = document.querySelector('.payment-section');
    paymentSection.insertBefore(errorDiv, paymentSection.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Alternative Payment Methods
function handlePayPalPayment() {
    showProcessingModal();
    
    // Simulate PayPal redirect
    setTimeout(() => {
        hideProcessingModal();
        alert('Redirecting to PayPal...');
        // In real implementation, redirect to PayPal
    }, 2000);
}

function handleApplePayPayment() {
    if ('ApplePaySession' in window) {
        // Real Apple Pay integration would go here
        showProcessingModal();
        setTimeout(() => {
            processPaymentSuccess();
        }, 2000);
    } else {
        showError('Apple Pay is not available on this device.');
    }
}

function handleGooglePayPayment() {
    // Real Google Pay integration would go here
    showProcessingModal();
    setTimeout(() => {
        processPaymentSuccess();
    }, 2000);
}

function processPaymentSuccess() {
    hideProcessingModal();
    localStorage.removeItem('checkoutFormData');
    window.location.href = 'order-confirmation.html';
}

// Event Listeners for Alternative Payment Methods
document.addEventListener('DOMContentLoaded', function() {
    const paypalBtn = document.querySelector('.paypal-btn');
    const applePayBtn = document.querySelector('.apple-pay-btn');
    const googlePayBtn = document.querySelector('.google-pay-btn');
    
    if (paypalBtn) {
        paypalBtn.addEventListener('click', handlePayPalPayment);
    }
    
    if (applePayBtn) {
        applePayBtn.addEventListener('click', handleApplePayPayment);
    }
    
    if (googlePayBtn) {
        googlePayBtn.addEventListener('click', handleGooglePayPayment);
    }
});

// Additional CSS for dynamic elements
const additionalCSS = `
    .field-error {
        color: #e74c3c;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        display: block;
    }
    
    .payment-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: slideDown 0.3s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .highlight {
        animation: highlight 0.6s ease-in-out;
    }
    
    @keyframes highlight {
        0%, 100% {
            background-color: transparent;
        }
        50% {
            background-color: #fff3cd;
        }
    }
`;

// Add the CSS to the page
const styleElement = document.createElement('style');
styleElement.textContent = additionalCSS;
document.head.appendChild(styleElement);
