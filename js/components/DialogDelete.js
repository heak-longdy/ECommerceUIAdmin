// DialogDelete Alpine.js Component
// A dedicated component for handling delete confirmation dialogs

document.addEventListener('alpine:init', () => {
    Alpine.data('DialogDelete', () => ({
        // Initialize the component
        init() {
            console.log('hello');
        },

        // Component state
        showDeleteDialog: false,
        dialogConfig: null,

        // Methods
        showDialog(config = {}) {
            this.dialogConfig = {
                title: config.title || 'Confirm Delete',
                message: config.message || 'Are you sure you want to delete this item?',
                icon: config.icon || 'delete',
                iconBackground: config.iconBackground || 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                iconShadow: config.iconShadow || '0 8px 24px rgba(239, 68, 68, 0.3)',
                primaryButton: {
                    text: config.primaryButton?.text || 'Delete',
                    style: config.primaryButton?.style || 'background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white;',
                    action: config.primaryButton?.action || this.confirmDelete.bind(this)
                },
                secondaryButton: {
                    text: config.secondaryButton?.text || 'Cancel',
                    style: config.secondaryButton?.style || 'background: #f3f4f6; color: #374151;',
                    action: config.secondaryButton?.action || this.cancelDelete.bind(this)
                },
                additionalButton: config.additionalButton || null,
                ...config
            };
            this.showDeleteDialog = true;
        },

        confirmDelete() {
            if (this.dialogConfig?.primaryButton?.action && typeof this.dialogConfig.primaryButton.action === 'function') {
                this.dialogConfig.primaryButton.action();
            }
            this.hideDialog();
        },

        cancelDelete() {
            if (this.dialogConfig?.secondaryButton?.action && typeof this.dialogConfig.secondaryButton.action === 'function') {
                this.dialogConfig.secondaryButton.action();
            }
            this.hideDialog();
        },

        handleAdditionalAction() {
            if (this.dialogConfig?.additionalButton?.action && typeof this.dialogConfig.additionalButton.action === 'function') {
                this.dialogConfig.additionalButton.action();
            }
            this.hideDialog();
        },

        hideDialog() {
            this.showDeleteDialog = false;
            this.dialogConfig = null;
        },

        // Predefined dialog configurations
        showDeleteConfirmation(itemName = 'item') {
            this.showDialog({
                title: 'Delete Confirmation',
                message: `Are you sure you want to delete this ${itemName}? This action cannot be undone.`,
                icon: 'delete_forever',
                primaryButton: {
                    text: 'Delete',
                    action: () => {
                        console.log(`Deleting ${itemName}...`);
                        // Add your delete logic here
                    }
                }
            });
        },

        showArchiveConfirmation(itemName = 'item') {
            this.showDialog({
                title: 'Archive Confirmation',
                message: `Are you sure you want to archive this ${itemName}?`,
                icon: 'archive',
                iconBackground: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                iconShadow: '0 8px 24px rgba(245, 158, 11, 0.3)',
                primaryButton: {
                    text: 'Archive',
                    style: 'background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white;',
                    action: () => {
                        console.log(`Archiving ${itemName}...`);
                        // Add your archive logic here
                    }
                }
            });
        },

        showCompleteConfirmation(itemName = 'item') {
            this.showDialog({
                title: 'Mark as Complete',
                message: `Are you sure you want to mark this ${itemName} as complete?`,
                icon: 'check_circle',
                iconBackground: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                iconShadow: '0 8px 24px rgba(16, 185, 129, 0.3)',
                primaryButton: {
                    text: 'Complete',
                    style: 'background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white;',
                    action: () => {
                        console.log(`Completing ${itemName}...`);
                        // Add your complete logic here
                    }
                }
            });
        }
    }));
});
