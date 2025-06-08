// Purchase Order functionality
document.addEventListener('DOMContentLoaded', function() {
    // Quantity controls
    const qtyBtns = document.querySelectorAll('.qty-btn');
    qtyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const row = this.closest('.product-row');
            const qtySpan = row.querySelector('.quantity-controls span');
            const unitPrice = parseFloat(row.querySelector('td:nth-child(2)').textContent.replace('$', ''));
            const totalCell = row.querySelector('td:nth-child(4)');
            
            let currentQty = parseInt(qtySpan.textContent);
            
            if (this.textContent === '+') {
                currentQty++;
            } else if (this.textContent === '-' && currentQty > 1) {
                currentQty--;
            }
            
            qtySpan.textContent = currentQty;
            const newTotal = unitPrice * currentQty;
            totalCell.textContent = '$' + newTotal.toLocaleString();
            
            updateOrderSummary();
        });
    });
    
    // Delivery company selection
    const deliveryCompanies = document.querySelectorAll('.delivery-company');
    deliveryCompanies.forEach(company => {
        company.addEventListener('click', function() {
            deliveryCompanies.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    
    // Button interactions
    const receiveBtn = document.querySelector('.receive-btn');
    const sendBtn = document.querySelector('.send-btn');
    const rejectBtn = document.querySelector('.reject-btn');
    const shipBtn = document.querySelector('.ship-btn');
    
    if (receiveBtn) {
        receiveBtn.addEventListener('click', function() {
            alert('Payment received successfully!');
            this.style.background = '#28a745';
            this.textContent = 'Payment Received ✓';
            this.disabled = true;
        });
    }
    
    if (sendBtn) {
        sendBtn.addEventListener('click', function() {
            const selectedCompany = document.querySelector('.delivery-company.selected');
            if (selectedCompany) {
                alert(`Order sent to ${selectedCompany.textContent} for delivery!`);
                this.style.background = '#6c757d';
                this.textContent = 'Sent to Delivery ✓';
                this.disabled = true;
            } else {
                alert('Please select a delivery company first.');
            }
        });
    }
    
    if (rejectBtn) {
        rejectBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to reject this order?')) {
                alert('Order has been rejected.');
                document.querySelector('.container').style.opacity = '0.5';
            }
        });
    }
    
    if (shipBtn) {
        shipBtn.addEventListener('click', function() {
            alert('Order is being prepared for shipping!');
            updateProgressTracker('shipping');
        });
    }
    
    function updateOrderSummary() {
        // Calculate totals from all product rows
        const productRows = document.querySelectorAll('.product-row');
        let subtotal = 0;
        
        productRows.forEach(row => {
            const total = parseFloat(row.querySelector('td:nth-child(4)').textContent.replace('$', '').replace(',', ''));
            subtotal += total;
        });
        
        // Update summary (you can adjust these calculations as needed)
        const discount = subtotal * 0.10; // 10% discount
        const tax = subtotal * 0.08; // 8% tax
        const promoDiscount = 100; // $100 promo code
        
        const finalTotal = subtotal - discount + tax - promoDiscount;
        
        // Update summary rows if they exist
        const summaryRows = document.querySelectorAll('.summary-row');
        if (summaryRows.length > 0) {
            // Update the displayed values
            console.log(`Subtotal: $${subtotal}, Final: $${finalTotal}`);
        }
    }
    
    function updateProgressTracker(stage) {
        const steps = document.querySelectorAll('.progress-step');
        const stepIcons = document.querySelectorAll('.step-icon');
        
        stepIcons.forEach((icon, index) => {
            if (index <= getStageIndex(stage)) {
                icon.className = 'step-icon completed';
            } else {
                icon.className = 'step-icon pending';
            }
        });
    }
    
    function getStageIndex(stage) {
        const stages = ['placed', 'packaging', 'shipping', 'received'];
        return stages.indexOf(stage);
    }
    
    // Initialize order summary
    updateOrderSummary();
});
