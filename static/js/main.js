/**
 * Social Stories App - Main JavaScript Module
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    SocialStoriesApp.init();
});

const SocialStoriesApp = {
    init() {
        this.setupAlerts();
        this.setupForms();
        this.setupNavigation();
        this.setupStoryFeatures();
        this.setupAccessibility();
        console.log('Social Stories App initialized successfully!');
    },

    /**
     * Setup auto-dismissing alerts
     */
    setupAlerts() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        
        alerts.forEach(alert => {
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alert && alert.parentNode) {
                    alert.style.opacity = '0';
                    alert.style.transition = 'opacity 0.3s ease';
                    setTimeout(() => {
                        alert.remove();
                    }, 300);
                }
            }, 5000);
        });
    },

    /**
     * Setup form enhancements
     */
    setupForms() {
        // Character counter for textareas
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            this.addCharacterCounter(textarea);
        });

        // Form validation feedback
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });

        // Auto-save for story content (draft functionality)
        const storyForm = document.querySelector('#story-form');
        if (storyForm) {
            this.setupAutoSave(storyForm);
        }
    },

    /**
     * Add character counter to textarea
     */
    addCharacterCounter(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        if (!maxLength) return;

        const counter = document.createElement('small');
        counter.className = 'form-text text-muted char-counter';
        counter.textContent = `0 / ${maxLength} characters`;
        
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', () => {
            const currentLength = textarea.value.length;
            counter.textContent = `${currentLength} / ${maxLength} characters`;
            
            // Change colour when nearing limit
            if (currentLength > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
        });
    },

    /**
     * Handle form submission with loading states
     */
    handleFormSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (submitBtn) {
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...';
            
            // Re-enable after 10 seconds as fallback
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }, 10000);
        }
    },

    /**
     * Setup navigation enhancements
     */
    setupNavigation() {
        // Highlight current page in navigation
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });

        // Mobile menu toggle
        const navbarToggler = document.querySelector('.navbar-toggler');
        if (navbarToggler) {
            navbarToggler.addEventListener('click', () => {
                const navbarCollapse = document.querySelector('.navbar-collapse');
                navbarCollapse.classList.toggle('show');
            });
        }
    },

    /**
     * Setup story-specific features
     */
    setupStoryFeatures() {
        // Confirm deletion
        const deleteButtons = document.querySelectorAll('.btn-delete-story');
        deleteButtons.forEach(button => {
            button.addEventListener('click', this.confirmDelete.bind(this));
        });

        // Story preview
        const previewButtons = document.querySelectorAll('.btn-preview-story');
        previewButtons.forEach(button => {
            button.addEventListener('click', this.showPreview.bind(this));
        });

        // Copy story link
        const copyButtons = document.querySelectorAll('.btn-copy-link');
        copyButtons.forEach(button => {
            button.addEventListener('click', this.copyToClipboard.bind(this));
        });
    },

    /**
     * Confirm story deletion
     */
    confirmDelete(event) {
        event.preventDefault();
        const button = event.target.closest('.btn-delete-story');
        const storyTitle = button.dataset.storyTitle || 'this story';
        
        if (confirm(`Are you sure you want to delete "${storyTitle}"? This action cannot be undone.`)) {
            // Find and submit the delete form
            const form = button.closest('form') || document.querySelector(`form[data-story-id="${button.dataset.storyId}"]`);
            if (form) {
                form.submit();
            }
        }
    },

    /**
     * Show story preview modal
     */
    showPreview(event) {
        const button = event.target.closest('.btn-preview-story');
        const storyId = button.dataset.storyId;
        
        // This would typically load story content via AJAX
        // For now, we'll use the content from the page
        const storyContent = document.querySelector(`[data-story-content="${storyId}"]`);
        if (storyContent) {
            this.showModal('Story Preview', storyContent.innerHTML);
        }
    },

    /**
     * Copy text to clipboard
     */
    async copyToClipboard(event) {
        const button = event.target.closest('.btn-copy-link');
        const textToCopy = button.dataset.copyText || window.location.href;
        
        try {
            await navigator.clipboard.writeText(textToCopy);
            this.showToast('Link copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy text: ', err);
            this.showToast('Failed to copy link', 'error');
        }
    },

    /**
     * Setup auto-save functionality
     */
    setupAutoSave(form) {
        const titleInput = form.querySelector('#title');
        const contentTextarea = form.querySelector('#content');
        
        if (!titleInput || !contentTextarea) return;

        let autoSaveTimer;
        const autoSaveDelay = 3000; // 3 seconds

        const saveData = () => {
            const data = {
                title: titleInput.value,
                content: contentTextarea.value,
                timestamp: new Date().toISOString()
            };
            
            localStorage.setItem('story-draft', JSON.stringify(data));
            this.showToast('Draft saved', 'info', 2000);
        };

        const handleInput = () => {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(saveData, autoSaveDelay);
        };

        titleInput.addEventListener('input', handleInput);
        contentTextarea.addEventListener('input', handleInput);

        // Load saved draft on page load
        this.loadDraft(titleInput, contentTextarea);
    },

    /**
     * Load saved draft
     */
    loadDraft(titleInput, contentTextarea) {
        const saved = localStorage.getItem('story-draft');
        if (saved && (!titleInput.value && !contentTextarea.value)) {
            try {
                const data = JSON.parse(saved);
                if (confirm('A draft was found. Would you like to restore it?')) {
                    titleInput.value = data.title || '';
                    contentTextarea.value = data.content || '';
                }
            } catch (err) {
                console.error('Failed to load draft:', err);
            }
        }
    },

    /**
     * Setup accessibility features
     */
    setupAccessibility() {
        // Skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'sr-only sr-only-focusable btn btn-primary';
        skipLink.textContent = 'Skip to main content';
        skipLink.style.position = 'absolute';
        skipLink.style.top = '10px';
        skipLink.style.left = '10px';
        skipLink.style.zIndex = '9999';
        
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Keyboard navigation for custom components
        this.setupKeyboardNavigation();
    },

    /**
     * Setup keyboard navigation
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (event) => {
            // ESC to close modals
            if (event.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const closeBtn = modal.querySelector('.btn-close');
                    if (closeBtn) closeBtn.click();
                });
            }
        });
    },

    /**
     * Show toast notification
     */
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, duration);
    },

    /**
     * Show modal dialog
     */
    showModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal fade show';
        modal.style.display = 'block';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal on click outside or close button
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.matches('.btn-close')) {
                modal.remove();
            }
        });
    }
};