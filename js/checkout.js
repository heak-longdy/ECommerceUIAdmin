// Checkout Page JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeCheckout();
});

function initializeCheckout() {
    // Initialize form validation
    setupFormValidation();
    
    // Setup shipping options
    setupShippingOptions();
    
    // Setup billing address toggle
    setupBillingToggle();
    
    // Setup promo code functionality
    setupPromoCode();
    
    // Initialize animations
    addPageAnimations();
    
    // Setup form auto-save
    setupAutoSave();
}

// Form Validation
function setupFormValidation() {
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    
    requiredFields.forEach(field => {
        field.addEventListener('blur', validateField);
        field.addEventListener('input', clearFieldError);
    });
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    // Remove existing error styling
    field.classList.remove('error');
    removeFieldError(field);
    
    // Check if field is empty
    if (!value) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    // Specific validation rules
    switch(field.type) {
        case 'email':
            if (!isValidEmail(value)) {
                showFieldError(field, 'Please enter a valid email address');
                return false;
            }
            break;
        case 'tel':
            if (!isValidPhone(value)) {
                showFieldError(field, 'Please enter a valid phone number');
                return false;
            }
            break;
        case 'text':
            if (field.name.includes('zip') || field.name.includes('postal')) {
                if (!isValidZip(value)) {
                    showFieldError(field, 'Please enter a valid ZIP code');
                    return false;
                }
            }
            break;
    }
    
    // Add success styling
    field.classList.add('valid');
    return true;
}

function clearFieldError(e) {
    const field = e.target;
    field.classList.remove('error');
    removeFieldError(field);
}

function showFieldError(field, message) {
    field.classList.add('error');
    
    // Create error message element
    const errorElement = document.createElement('span');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    
    // Insert after the field
    field.parentNode.insertBefore(errorElement, field.nextSibling);
}

function removeFieldError(field) {
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
}

// Validation helper functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    const cleanPhone = phone.replace(/[\s\-\(\)]/g, '');
    return phoneRegex.test(cleanPhone) && cleanPhone.length >= 10;
}

function isValidZip(zip) {
    const zipRegex = /^\d{5}(-\d{4})?$/;
    return zipRegex.test(zip);
}

// Shipping Options
function setupShippingOptions() {
    const shippingOptions = document.querySelectorAll('input[name="shipping"]');
    const shippingCostElement = document.getElementById('shipping-cost');
    const finalTotalElement = document.getElementById('final-total');
    
    shippingOptions.forEach(option => {
        option.addEventListener('change', updateShippingCost);
    });
    
    function updateShippingCost() {
        const selectedOption = document.querySelector('input[name="shipping"]:checked');
        let shippingCost = 0;
        let shippingText = 'Free';
        
        switch(selectedOption.value) {
            case 'express':
                shippingCost = 9.99;
                shippingText = '$9.99';
                break;
            case 'overnight':
                shippingCost = 24.99;
                shippingText = '$24.99';
                break;
            default:
                shippingCost = 0;
                shippingText = 'Free';
        }
        
        shippingCostElement.textContent = shippingText;
        updateFinalTotal();
        
        // Add animation to highlight the change
        shippingCostElement.classList.add('highlight');
        setTimeout(() => {
            shippingCostElement.classList.remove('highlight');
        }, 1000);
    }
}

// Billing Address Toggle
function setupBillingToggle() {
    const sameAsShippingCheckbox = document.getElementById('same-as-shipping');
    const billingForm = document.getElementById('billing-form');
    
    sameAsShippingCheckbox.addEventListener('change', function() {
        if (this.checked) {
            billingForm.classList.add('hidden');
            copyShippingToBilling();
        } else {
            billingForm.classList.remove('hidden');
            billingForm.classList.add('fade-in');
        }
    });
}

function copyShippingToBilling() {
    const shippingFields = {
        'first-name': 'billing-first-name',
        'last-name': 'billing-last-name',
        'address': 'billing-address',
        'city': 'billing-city',
        'state': 'billing-state',
        'zip': 'billing-zip'
    };
    
    Object.keys(shippingFields).forEach(shippingId => {
        const shippingField = document.getElementById(shippingId);
        const billingField = document.getElementById(shippingFields[shippingId]);
        
        if (shippingField && billingField) {
            billingField.value = shippingField.value;
        }
    });
}

// Promo Code Functionality
function setupPromoCode() {
    const promoInput = document.getElementById('promo-code');
    const applyBtn = document.querySelector('.apply-btn');
    
    applyBtn.addEventListener('click', applyPromoCode);
    
    promoInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            applyPromoCode();
        }
    });
}

function applyPromoCode() {
    const promoInput = document.getElementById('promo-code');
    const promoCode = promoInput.value.trim().toUpperCase();
    const applyBtn = document.querySelector('.apply-btn');
    
    // Show loading state
    applyBtn.classList.add('loading');
    applyBtn.textContent = 'Applying...';
    
    // Simulate API call
    setTimeout(() => {
        const validCodes = {
            'SAVE10': { discount: 10, type: 'percentage' },
            'WELCOME50': { discount: 50, type: 'fixed' },
            'NEWUSER': { discount: 15, type: 'percentage' }
        };
        
        if (validCodes[promoCode]) {
            const discount = validCodes[promoCode];
            applyDiscount(discount);
            showPromoSuccess('Promo code applied successfully!');
            promoInput.disabled = true;
            applyBtn.textContent = 'Applied';
            applyBtn.disabled = true;
        } else {
            showPromoError('Invalid promo code');
        }
        
        applyBtn.classList.remove('loading');
    }, 1500);
}

function applyDiscount(discount) {
    const discountRow = document.querySelector('.total-row.discount');
    const subtotal = 529.98; // This would be calculated dynamically
    
    let discountAmount = 0;
    if (discount.type === 'percentage') {
        discountAmount = subtotal * (discount.discount / 100);
    } else {
        discountAmount = discount.discount;
    }
    
    discountRow.querySelector('span:last-child').textContent = `-$${discountAmount.toFixed(2)}`;
    discountRow.classList.remove('hidden');
    discountRow.classList.add('slide-in');
    
    updateFinalTotal();
}

function showPromoSuccess(message) {
    showPromoMessage(message, 'success');
}

function showPromoError(message) {
    showPromoMessage(message, 'error');
}

function showPromoMessage(message, type) {
    // Remove existing messages
    const existingMessage = document.querySelector('.promo-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const messageElement = document.createElement('div');
    messageElement.className = `promo-message ${type}`;
    messageElement.textContent = message;
    
    const promoSection = document.querySelector('.promo-section');
    promoSection.appendChild(messageElement);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (messageElement.parentNode) {
            messageElement.remove();
        }
    }, 3000);
}

// Update Final Total
function updateFinalTotal() {
    const subtotal = 529.98;
    const tax = 42.40;
    const shippingCost = getShippingCost();
    const discount = getDiscountAmount();
    
    const finalTotal = subtotal + tax + shippingCost - discount;
    
    document.getElementById('final-total').textContent = `$${finalTotal.toFixed(2)}`;
}

function getShippingCost() {
    const selectedShipping = document.querySelector('input[name="shipping"]:checked');
    if (!selectedShipping) return 0;
    
    switch(selectedShipping.value) {
        case 'express': return 9.99;
        case 'overnight': return 24.99;
        default: return 0;
    }
}

function getDiscountAmount() {
    const discountRow = document.querySelector('.total-row.discount');
    if (discountRow.classList.contains('hidden')) return 0;
    
    const discountText = discountRow.querySelector('span:last-child').textContent;
    return parseFloat(discountText.replace(/[$-]/g, '')) || 0;
}

// Page Animations
function addPageAnimations() {
    // Add stagger animation to form sections
    const sections = document.querySelectorAll('.checkout-section');
    sections.forEach((section, index) => {
        section.style.animationDelay = `${index * 0.1}s`;
        section.classList.add('fade-in');
    });
    
    // Add animation to order summary
    const orderSummary = document.querySelector('.order-summary');
    if (orderSummary) {
        orderSummary.style.animationDelay = '0.3s';
        orderSummary.classList.add('fade-in');
    }
}

// Auto-save functionality
function setupAutoSave() {
    const formFields = document.querySelectorAll('input, select');
    
    formFields.forEach(field => {
        field.addEventListener('change', saveFormData);
        field.addEventListener('input', debounce(saveFormData, 1000));
    });
    
    // Load saved data on page load
    loadFormData();
}

function saveFormData() {
    const formData = {};
    const formFields = document.querySelectorAll('input, select');
    
    formFields.forEach(field => {
        if (field.type !== 'radio' || field.checked) {
            formData[field.name || field.id] = field.value;
        }
    });
    
    localStorage.setItem('checkoutFormData', JSON.stringify(formData));
}

function loadFormData() {
    const savedData = localStorage.getItem('checkoutFormData');
    if (!savedData) return;
    
    try {
        const formData = JSON.parse(savedData);
        
        Object.keys(formData).forEach(key => {
            const field = document.querySelector(`[name="${key}"], #${key}`);
            if (field) {
                if (field.type === 'radio') {
                    if (field.value === formData[key]) {
                        field.checked = true;
                    }
                } else {
                    field.value = formData[key];
                }
            }
        });
        
        // Update shipping cost if shipping method was loaded
        updateFinalTotal();
    } catch (error) {
        console.error('Error loading saved form data:', error);
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Proceed to Payment
function proceedToPayment() {
    // Validate all required fields
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateField({ target: field })) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        // Scroll to first error
        const firstError = document.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        showErrorMessage('Please fill in all required fields correctly.');
        return;
    }
    
    // Show loading state
    const continueBtn = document.querySelector('.btn-primary');
    continueBtn.classList.add('loading');
    continueBtn.textContent = 'Processing...';
    
    // Simulate processing
    setTimeout(() => {
        // Clear saved form data
        localStorage.removeItem('checkoutFormData');
        
        // Redirect to payment page
        window.location.href = 'payment.html';
    }, 2000);
}

function showErrorMessage(message) {
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
    `;
    
    // Insert at top of checkout forms
    const checkoutForms = document.querySelector('.checkout-forms');
    checkoutForms.insertBefore(errorDiv, checkoutForms.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Add additional CSS for dynamic elements
const additionalCSS = `
    .field-error {
        color: #e74c3c;
        font-size: 0.8rem;
        margin-top: 0.25rem;
        display: block;
    }
    
    .form-group input.error,
    .form-group select.error {
        border-color: #e74c3c;
        box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
    }
    
    .form-group input.valid,
    .form-group select.valid {
        border-color: #27ae60;
    }
    
    .highlight {
        background: #fff3cd !important;
        transition: background 0.3s ease;
    }
    
    .promo-message {
        padding: 0.75rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .promo-message.success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .promo-message.error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .apply-btn:disabled {
        background: #6c757d;
        cursor: not-allowed;
    }
    
    .promo-input input:disabled {
        background: #f8f9fa;
        cursor: not-allowed;
    }
`;

// Add the CSS to the page
const styleElement = document.createElement('style');
styleElement.textContent = additionalCSS;
document.head.appendChild(styleElement);
