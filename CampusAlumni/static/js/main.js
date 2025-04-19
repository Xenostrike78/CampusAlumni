/**
 * CampusAlumni - Main JavaScript File
 * Contains minimal JS functionality for user interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initializeNavbar();
    initializePasswordToggle();
    initializeFormSections();
    initializeViewSwitcher();
    initializeSearchBar();
    initializeCardFlip();
    initializeScrollAnimations();
    initializeProfileTabs();
    initializeAchievementProgress();
});

/**
 * Toggle mobile bottom navbar visibility based on scroll direction
 */
function initializeNavbar() {
    const bottomNav = document.querySelector('.bottom-nav');
    if (!bottomNav) return;
    
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;
        
        // Determine scroll direction
        if (currentScrollY > lastScrollY) {
            // Scrolling down - hide navbar
            bottomNav.style.transform = 'translateY(100%)';
        } else {
            // Scrolling up - show navbar
            bottomNav.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

/**
 * Toggle password visibility in login/signup forms
 */
function initializePasswordToggle() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordField = document.getElementById(this.id.replace('-toggle', ''));
            
            // Toggle password visibility
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            } else {
                passwordField.type = 'password';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            }
        });
    });
}

/**
 * Initialize collapsible sections in the edit profile page
 */
function initializeFormSections() {
    const sectionTitles = document.querySelectorAll('.form-section-title');
    
    sectionTitles.forEach(title => {
        title.addEventListener('click', function() {
            // Toggle the collapsed class
            this.classList.toggle('collapsed');
            
            // Find the content section
            const content = this.nextElementSibling;
            content.classList.toggle('collapsed');
        });
    });
}

/**
 * Initialize view switcher between grid and list views in alumni directory
 */
function initializeViewSwitcher() {
    const viewButtons = document.querySelectorAll('.view-mode-btn');
    if (!viewButtons.length) return;
    
    const alumniGrid = document.querySelector('.alumni-grid');
    const alumniList = document.querySelector('.alumni-list');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            viewButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Switch view based on data-view attribute
            const viewMode = this.getAttribute('data-view');
            
            if (viewMode === 'grid') {
                alumniGrid.style.display = 'grid';
                alumniList.style.display = 'none';
            } else if (viewMode === 'list') {
                alumniGrid.style.display = 'none';
                alumniList.style.display = 'block';
            }
        });
    });
}

/**
 * Initialize expandable search bar
 */
function initializeSearchBar() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        // Focus event expands the search bar
        input.addEventListener('focus', function() {
            this.style.width = '200px';
        });
        
        // Blur event collapses the search bar if empty
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.width = '40px';
            }
        });
    });
}

/**
 * Initialize card flip effect for alumni directory cards
 */
function initializeCardFlip() {
    // This is handled by CSS for smooth transitions
    // This function is a placeholder for any additional JS-based card flip functionality
}

/**
 * Initialize scroll animations for elements
 */
function initializeScrollAnimations() {
    // Circular progress in achievements
    const circularProgress = document.querySelectorAll('.circular-progress');
    
    if (circularProgress.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Get progress value from CSS variable
                    const progressValue = entry.target.style.getPropertyValue('--progress');
                    
                    // Animate the inner circle text
                    const innerCircle = entry.target.querySelector('.inner-circle');
                    if (innerCircle) {
                        const targetValue = parseInt(progressValue);
                        let currentValue = 0;
                        
                        const interval = setInterval(() => {
                            if (currentValue >= targetValue) {
                                clearInterval(interval);
                            } else {
                                currentValue += 1;
                                innerCircle.textContent = currentValue + '%';
                            }
                        }, 20);
                    }
                    
                    // Stop observing once animation is triggered
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        circularProgress.forEach(progress => {
            observer.observe(progress);
        });
    }
    
    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-bar .progress');
    
    if (progressBars.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Get width from inline style or data attribute
                    const widthValue = entry.target.style.width || entry.target.dataset.width || '0%';
                    entry.target.style.setProperty('--width', widthValue);
                    
                    // Stop observing once animation is triggered
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        progressBars.forEach(progress => {
            observer.observe(progress);
        });
    }
}

/**
 * Initialize tabs in profile page and other tabbed interfaces
 */
function initializeProfileTabs() {
    const tabSets = [
        { tabs: '.profile-tab', content: '.profile-content section' },
        { tabs: '.mentorship-tab', content: '.mentorship-content section' },
        { tabs: '.achievements-tab', content: '.achievements-content section' },
        { tabs: '.network-tab', content: '.network-content section' }
    ];
    
    tabSets.forEach(tabSet => {
        const tabs = document.querySelectorAll(tabSet.tabs);
        
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding content
                const tabId = this.getAttribute('data-tab');
                const contentSections = document.querySelectorAll(tabSet.content);
                
                contentSections.forEach(section => {
                    if (section.getAttribute('data-tab') === tabId) {
                        section.style.display = 'block';
                    } else {
                        section.style.display = 'none';
                    }
                });
            });
        });
    });
}

/**
 * Initialize progress animations in achievements page
 */
function initializeAchievementProgress() {
    // Progress bar on scroll
    const progressBar = document.querySelector('.edit-form-progress .progress-bar');
    
    if (progressBar) {
        window.addEventListener('scroll', function() {
            const scrollTop = document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight;
            const clientHeight = document.documentElement.clientHeight;
            
            const scrollPercentage = (scrollTop / (scrollHeight - clientHeight)) * 100;
            
            progressBar.style.width = scrollPercentage + '%';
        });
    }
}

/**
 * Handle skill additions in the edit profile page
 */
document.addEventListener('DOMContentLoaded', function() {
    const addSkillBtn = document.querySelector('.skill-input-group .btn-add');
    const skillInput = document.getElementById('skillInput');
    const addedSkills = document.querySelector('.added-skills');
    
    if (addSkillBtn && skillInput && addedSkills) {
        addSkillBtn.addEventListener('click', function() {
            const skill = skillInput.value.trim();
            
            if (skill) {
                // Create new skill element
                const skillElement = document.createElement('div');
                skillElement.className = 'added-skill';
                skillElement.innerHTML = `${skill} <span class="remove-skill"><i class="fas fa-times"></i></span>`;
                
                // Add to DOM
                addedSkills.appendChild(skillElement);
                
                // Clear input
                skillInput.value = '';
                
                // Add event listener to remove button
                const removeBtn = skillElement.querySelector('.remove-skill');
                removeBtn.addEventListener('click', function() {
                    skillElement.remove();
                });
            }
        });
        
        // Allow adding skill with Enter key
        skillInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addSkillBtn.click();
            }
        });
    }
    
    // Handle removing existing skills
    const removeSkillBtns = document.querySelectorAll('.remove-skill');
    removeSkillBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
});

/**
 * Modal functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            
            if (modal) {
                modal.classList.add('active');
                
                // Close button functionality
                const closeBtn = modal.querySelector('.modal-close');
                if (closeBtn) {
                    closeBtn.addEventListener('click', function() {
                        modal.classList.remove('active');
                    });
                }
                
                // Close on click outside
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        modal.classList.remove('active');
                    }
                });
            }
        });
    });
});

/**
 * Post input trigger for creating new posts
 */
document.addEventListener('DOMContentLoaded', function() {
    const postInputTrigger = document.getElementById('post-input-trigger');
    
    if (postInputTrigger) {
        postInputTrigger.addEventListener('click', function() {
            alert('This would open a post creation modal in a full implementation');
        });
    }
});

/**
 * Handle filter tag removal
 */
document.addEventListener('DOMContentLoaded', function() {
    const filterTagRemoveBtns = document.querySelectorAll('.tag-remove');
    
    filterTagRemoveBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
});
