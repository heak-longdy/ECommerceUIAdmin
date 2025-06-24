// Order Confirmation Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeConfirmationPage();
});

function initializeConfirmationPage() {
    generateOrderId();
    setupAnimations();
    setupInteractiveElements();
    updateDeliveryEstimate();
    trackPageView();
}

// Generate a unique order ID
function generateOrderId() {
    const orderIdElement = document.getElementById('order-id');
    if (orderIdElement) {
        const currentDate = new Date();
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(currentDate.getDate()).padStart(2, '0');
        const randomNum = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
        
        const orderId = `ECM-${year}${month}${day}-${randomNum}`;
        orderIdElement.textContent = orderId;
        
        // Save order ID to localStorage for future reference
        localStorage.setItem('lastOrderId', orderId);
    }
}

// Setup page animations
function setupAnimations() {
    // Add staggered animations to main content
    const orderDetails = document.querySelector('.order-details');
    const sidebar = document.querySelector('.confirmation-sidebar');
    
    if (orderDetails) {
        orderDetails.classList.add('stagger-animation');
    }
    
    if (sidebar) {
        setTimeout(() => {
            sidebar.classList.add('fade-in-up');
        }, 300);
    }
    
    // Animate success banner elements
    animateSuccessBanner();
}

function animateSuccessBanner() {
    const successIcon = document.querySelector('.success-icon');
    const successTitle = document.querySelector('.success-banner h1');
    const successDescription = document.querySelector('.success-banner p');
    const orderNumber = document.querySelector('.order-number');
    
    // Stagger the animations
    if (successIcon) {
        successIcon.style.animationDelay = '0.2s';
    }
    
    if (successTitle) {
        successTitle.style.animation = 'fadeInUp 0.6s ease-out 0.4s backwards';
    }
    
    if (successDescription) {
        successDescription.style.animation = 'fadeInUp 0.6s ease-out 0.6s backwards';
    }
    
    if (orderNumber) {
        orderNumber.style.animation = 'fadeInUp 0.6s ease-out 0.8s backwards';
    }
}

// Setup interactive elements
function setupInteractiveElements() {
    setupCreateAccountButton();
    setupSupportOptions();
    setupNewsletterForm();
    setupTrackingUpdates();
}

function setupCreateAccountButton() {
    const createAccountBtn = document.querySelector('.btn-primary');
    
    if (createAccountBtn) {
        createAccountBtn.addEventListener('click', function() {
            // In a real application, this would open a registration modal or redirect
            showCreateAccountModal();
        });
    }
}

function showCreateAccountModal() {
    // Create a simple modal for account creation
    const modal = document.createElement('div');
    modal.className = 'account-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Create Your Account</h3>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <p>Create an account to track your orders and get exclusive benefits!</p>
                    <form class="account-form">
                        <div class="form-group">
                            <label for="account-email">Email Address</label>
                            <input type="email" id="account-email" required>
                        </div>
                        <div class="form-group">
                            <label for="account-password">Password</label>
                            <input type="password" id="account-password" required>
                        </div>
                        <div class="form-group">
                            <label for="account-confirm-password">Confirm Password</label>
                            <input type="password" id="account-confirm-password" required>
                        </div>
                        <button type="submit" class="btn-primary">Create Account</button>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal functionality
    const closeBtn = modal.querySelector('.close-btn');
    const overlay = modal.querySelector('.modal-overlay');
    
    closeBtn.addEventListener('click', () => modal.remove());
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) modal.remove();
    });
    
    // Form submission
    const form = modal.querySelector('.account-form');
    form.addEventListener('submit', handleAccountCreation);
}

function handleAccountCreation(e) {
    e.preventDefault();
    
    const email = document.getElementById('account-email').value;
    const password = document.getElementById('account-password').value;
    const confirmPassword = document.getElementById('account-confirm-password').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    
    // Simulate account creation
    setTimeout(() => {
        alert('Account created successfully! You can now track your orders.');
        document.querySelector('.account-modal').remove();
    }, 1000);
}

function setupSupportOptions() {
    const supportOptions = document.querySelectorAll('.support-option');
    
    supportOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            
            const supportType = this.querySelector('strong').textContent;
            handleSupportRequest(supportType);
        });
    });
}

function handleSupportRequest(type) {
    switch(type) {
        case 'Call Us':
            // In a real app, this might open a phone dialer or show phone number
            alert('Our support team is available at 1-800-SHOPEASE');
            break;
        case 'Live Chat':
            // In a real app, this would open a chat widget
            showChatWidget();
            break;
        case 'Email Support':
            // Open email client
            window.location.href = 'mailto:support@shopease.com?subject=Order Support Request';
            break;
    }
}

function showChatWidget() {
    // Simulate a chat widget
    const chatWidget = document.createElement('div');
    chatWidget.className = 'chat-widget';
    chatWidget.innerHTML = `
        <div class="chat-header">
            <h4>Live Chat Support</h4>
            <button class="chat-close">&times;</button>
        </div>
        <div class="chat-body">
            <div class="chat-message bot">
                <p>Hello! How can I help you with your order today?</p>
            </div>
        </div>
        <div class="chat-footer">
            <input type="text" placeholder="Type your message..." class="chat-input">
            <button class="chat-send">Send</button>
        </div>
    `;
    
    document.body.appendChild(chatWidget);
    
    // Chat functionality
    const closeBtn = chatWidget.querySelector('.chat-close');
    const sendBtn = chatWidget.querySelector('.chat-send');
    const input = chatWidget.querySelector('.chat-input');
    
    closeBtn.addEventListener('click', () => chatWidget.remove());
    sendBtn.addEventListener('click', sendChatMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
}

function sendChatMessage() {
    const input = document.querySelector('.chat-input');
    const chatBody = document.querySelector('.chat-body');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';
    userMessage.innerHTML = `<p>${message}</p>`;
    chatBody.appendChild(userMessage);
    
    input.value = '';
    
    // Simulate bot response
    setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'chat-message bot';
        botMessage.innerHTML = `<p>Thank you for your message. A support agent will assist you shortly.</p>`;
        chatBody.appendChild(botMessage);
        chatBody.scrollTop = chatBody.scrollHeight;
    }, 1000);
    
    chatBody.scrollTop = chatBody.scrollHeight;
}

function setupNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            if (email) {
                // Simulate newsletter subscription
                emailInput.value = '';
                showNotification('Successfully subscribed to newsletter!', 'success');
            }
        });
    }
}

function setupTrackingUpdates() {
    // Simulate tracking number generation after some time
    setTimeout(() => {
        const trackingPlaceholder = document.querySelector('.tracking-placeholder span');
        if (trackingPlaceholder) {
            const trackingNumber = generateTrackingNumber();
            trackingPlaceholder.innerHTML = `Tracking #: <strong>${trackingNumber}</strong>`;
            trackingPlaceholder.parentElement.style.borderColor = '#27ae60';
            trackingPlaceholder.parentElement.style.backgroundColor = '#f8fff9';
        }
    }, 5000);
}

function generateTrackingNumber() {
    const carriers = ['UPS', 'FDX', 'USPS'];
    const carrier = carriers[Math.floor(Math.random() * carriers.length)];
    const number = Math.random().toString(36).substr(2, 9).toUpperCase();
    return `${carrier}${number}`;
}

// Update delivery estimate based on current date
function updateDeliveryEstimate() {
    const deliveryElement = document.querySelector('.delivery-estimate strong');
    if (deliveryElement) {
        const startDate = new Date();
        startDate.setDate(startDate.getDate() + 5); // 5 days from now
        
        const endDate = new Date();
        endDate.setDate(endDate.getDate() + 7); // 7 days from now
        
        const options = { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric' 
        };
        
        const startFormatted = startDate.toLocaleDateString('en-US', options);
        const endFormatted = endDate.toLocaleDateString('en-US', options);
        
        deliveryElement.textContent = `${startFormatted} - ${endFormatted}`;
    }
}

// PDF Download functionality
function downloadPDF() {
    // In a real application, this would generate a PDF of the order
    showNotification('PDF download will be available soon!', 'info');
}

// Print functionality enhancement
function enhancePrintView() {
    const originalTitle = document.title;
    const orderId = document.getElementById('order-id').textContent;
    
    document.title = `Order ${orderId} - Receipt`;
    
    window.addEventListener('afterprint', () => {
        document.title = originalTitle;
    });
}

// Track page view for analytics
function trackPageView() {
    // In a real application, this would send analytics data
    console.log('Order confirmation page viewed');
    
    // Track conversion for marketing
    trackConversion();
}

function trackConversion() {
    const orderData = {
        orderId: document.getElementById('order-id').textContent,
        total: '$572.38',
        items: 2,
        timestamp: new Date().toISOString()
    };
    
    // In a real app, send this to analytics service
    console.log('Conversion tracked:', orderData);
    
    // Save conversion data locally
    localStorage.setItem('lastConversion', JSON.stringify(orderData));
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
    
    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => notification.remove());
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-triangle';
        case 'warning': return 'exclamation-circle';
        default: return 'info-circle';
    }
}

// Add dynamic CSS for new components
const dynamicCSS = `
    .account-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1000;
    }
    
    .modal-overlay {
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .modal-content {
        background: white;
        border-radius: 12px;
        max-width: 400px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    .modal-header h3 {
        margin: 0;
        color: #2c3e50;
    }
    
    .close-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        color: #6c757d;
        cursor: pointer;
    }
    
    .modal-body {
        padding: 1.5rem;
    }
    
    .account-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .account-form .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .account-form label {
        font-weight: 500;
        color: #2c3e50;
    }
    
    .account-form input {
        padding: 10px 12px;
        border: 2px solid #e9ecef;
        border-radius: 6px;
        font-size: 1rem;
    }
    
    .account-form input:focus {
        outline: none;
        border-color: #3498db;
    }
    
    .chat-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 300px;
        height: 400px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: #3498db;
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-header h4 {
        margin: 0;
    }
    
    .chat-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
    }
    
    .chat-body {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .chat-message {
        max-width: 80%;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    
    .chat-message.bot {
        background: #f1f3f4;
        align-self: flex-start;
    }
    
    .chat-message.user {
        background: #3498db;
        color: white;
        align-self: flex-end;
    }
    
    .chat-footer {
        padding: 1rem;
        border-top: 1px solid #e9ecef;
        display: flex;
        gap: 0.5rem;
    }
    
    .chat-input {
        flex: 1;
        padding: 8px 12px;
        border: 1px solid #e9ecef;
        border-radius: 6px;
    }
    
    .chat-send {
        padding: 8px 16px;
        background: #3498db;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 1000;
        min-width: 300px;
    }
    
    .notification.success {
        border-left: 4px solid #27ae60;
    }
    
    .notification.error {
        border-left: 4px solid #e74c3c;
    }
    
    .notification.warning {
        border-left: 4px solid #f39c12;
    }
    
    .notification.info {
        border-left: 4px solid #3498db;
    }
    
    .notification i {
        color: inherit;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: #6c757d;
        cursor: pointer;
        margin-left: auto;
    }
`;

// Add the CSS to the page
const styleElement = document.createElement('style');
styleElement.textContent = dynamicCSS;
document.head.appendChild(styleElement);

// Export functions for global access
window.downloadPDF = downloadPDF;
window.enhancePrintView = enhancePrintView;
