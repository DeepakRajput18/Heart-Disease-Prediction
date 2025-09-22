// Main Application JavaScript

class App {
    constructor() {
        this.currentUser = null;
        this.token = localStorage.getItem('token');
        this.apiBase = '/api';
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupTheme();
        this.checkAuth();
    }
    
    setupEventListeners() {
        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', this.toggleTheme.bind(this));
        
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const page = e.currentTarget.dataset.page;
                this.navigateTo(page);
            });
        });
        
        // Modal close events
        document.querySelectorAll('.close').forEach(close => {
            close.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                this.closeModal(modal.id);
            });
        });
        
        // Click outside modal to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal.id);
                }
            });
        });
    }
    
    setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.updateThemeIcon(newTheme);
        
        // Animate theme toggle
        gsap.to(document.getElementById('themeToggle'), {
            rotation: 360,
            duration: 0.5,
            ease: "back.out(1.7)"
        });
    }
    
    updateThemeIcon(theme) {
        const icon = document.querySelector('#themeToggle i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    checkAuth() {
        if (this.token) {
            this.validateToken();
        } else {
            this.showLogin();
        }
    }
    
    async validateToken() {
        try {
            const response = await this.apiCall('/dashboard/stats', 'GET');
            if (response.ok) {
                this.showDashboard();
            } else {
                this.logout();
            }
        } catch (error) {
            this.logout();
        }
    }
    
    showLogin() {
        this.showPage('loginPage');
        this.animateLogin();
    }
    
    showDashboard() {
        this.showPage('dashboardPage');
        this.animateDashboard();
        this.loadDashboardData();
    }
    
    showPage(pageId) {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        document.getElementById(pageId).classList.add('active');
    }
    
    navigateTo(page) {
        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-page="${page}"]`).classList.add('active');
        
        // Show content section
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${page}Content`).classList.add('active');
        
        // Load page-specific data
        this.loadPageData(page);
        
        // Animate page transition
        this.animatePageTransition(page);
    }
    
    loadPageData(page) {
        switch (page) {
            case 'dashboard':
                this.loadDashboardData();
                break;
            case 'patients':
                window.patientsManager.loadPatients();
                break;
            case 'predictions':
                window.predictionsManager.loadPredictions();
                break;
            case 'analytics':
                window.analyticsManager.loadAnalytics();
                break;
            case 'doctors':
                if (this.currentUser && this.currentUser.role === 'admin') {
                    this.loadDoctors();
                }
                break;
        }
    }
    
    async loadDashboardData() {
        try {
            this.showLoading();
            const stats = await this.apiCall('/dashboard/stats', 'GET');
            
            if (stats.ok) {
                const data = await stats.json();
                this.updateDashboardStats(data);
                this.loadDashboardCharts();
            }
        } catch (error) {
            this.showToast('Error loading dashboard data', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    updateDashboardStats(data) {
        document.getElementById('totalPatients').textContent = data.total_patients;
        document.getElementById('highRiskPatients').textContent = data.high_risk_patients;
        document.getElementById('recentPredictions').textContent = data.recent_predictions;
        document.getElementById('totalPredictions').textContent = data.total_predictions;
        
        // Animate counters
        this.animateCounters();
    }
    
    async loadDashboardCharts() {
        try {
            // Load risk distribution
            const riskData = await this.apiCall('/analytics/risk-distribution', 'GET');
            if (riskData.ok) {
                const data = await riskData.json();
                this.createRiskChart(data);
            }
            
            // Load timeline data
            const timelineData = await this.apiCall('/analytics/predictions-timeline', 'GET');
            if (timelineData.ok) {
                const data = await timelineData.json();
                this.createTimelineChart(data);
            }
        } catch (error) {
            console.error('Error loading charts:', error);
        }
    }
    
    createRiskChart(data) {
        const ctx = document.getElementById('riskChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.risk_level),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        'rgba(76, 175, 80, 0.8)',
                        'rgba(244, 67, 54, 0.8)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    createTimelineChart(data) {
        const ctx = document.getElementById('timelineChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => item.date),
                datasets: [{
                    label: 'Predictions',
                    data: data.map(item => item.count),
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    async loadDoctors() {
        try {
            this.showLoading();
            const response = await this.apiCall('/admin/doctors', 'GET');
            
            if (response.ok) {
                const doctors = await response.json();
                this.displayDoctors(doctors);
            }
        } catch (error) {
            this.showToast('Error loading doctors', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    displayDoctors(doctors) {
        const container = document.getElementById('doctorsGrid');
        container.innerHTML = '';
        
        doctors.forEach(doctor => {
            const doctorCard = this.createDoctorCard(doctor);
            container.appendChild(doctorCard);
        });
    }
    
    createDoctorCard(doctor) {
        const card = document.createElement('div');
        card.className = 'doctor-card fade-in-up';
        card.innerHTML = `
            <div class="doctor-header">
                <div class="doctor-avatar">
                    <i class="fas fa-user-md"></i>
                </div>
                <div class="doctor-info">
                    <h4>${doctor.name}</h4>
                    <p>${doctor.specialization}</p>
                </div>
            </div>
            <div class="doctor-details">
                <div class="doctor-detail">
                    <i class="fas fa-envelope"></i>
                    <span>${doctor.email}</span>
                </div>
                <div class="doctor-detail">
                    <i class="fas fa-user-tag"></i>
                    <span>${doctor.role}</span>
                </div>
                ${doctor.phone ? `
                    <div class="doctor-detail">
                        <i class="fas fa-phone"></i>
                        <span>${doctor.phone}</span>
                    </div>
                ` : ''}
            </div>
        `;
        return card;
    }
    
    // Animation methods
    animateLogin() {
        gsap.from('.login-card', {
            duration: 1,
            y: 50,
            opacity: 0,
            ease: "back.out(1.7)"
        });
        
        gsap.from('.shape', {
            duration: 2,
            scale: 0,
            opacity: 0,
            stagger: 0.2,
            ease: "elastic.out(1, 0.3)"
        });
    }
    
    animateDashboard() {
        gsap.from('.stat-card', {
            duration: 0.8,
            y: 30,
            opacity: 0,
            stagger: 0.1,
            ease: "power2.out"
        });
        
        gsap.from('.chart-container', {
            duration: 1,
            scale: 0.8,
            opacity: 0,
            stagger: 0.2,
            ease: "back.out(1.7)",
            delay: 0.5
        });
    }
    
    animatePageTransition(page) {
        const content = document.getElementById(`${page}Content`);
        gsap.from(content.children, {
            duration: 0.6,
            y: 20,
            opacity: 0,
            stagger: 0.1,
            ease: "power2.out"
        });
    }
    
    animateCounters() {
        document.querySelectorAll('.stat-content h3').forEach(counter => {
            const target = parseInt(counter.textContent);
            gsap.from({ value: 0 }, {
                duration: 2,
                value: target,
                ease: "power2.out",
                onUpdate: function() {
                    counter.textContent = Math.round(this.targets()[0].value);
                }
            });
        });
    }
    
    // Modal methods
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.classList.add('active');
        
        gsap.from(modal.querySelector('.modal-content'), {
            duration: 0.3,
            scale: 0.8,
            opacity: 0,
            ease: "back.out(1.7)"
        });
    }
    
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        
        gsap.to(modal.querySelector('.modal-content'), {
            duration: 0.2,
            scale: 0.8,
            opacity: 0,
            ease: "power2.in",
            onComplete: () => {
                modal.classList.remove('active');
            }
        });
    }
    
    // Utility methods
    showLoading() {
        document.getElementById('loadingSpinner').classList.add('active');
    }
    
    hideLoading() {
        document.getElementById('loadingSpinner').classList.remove('active');
    }
    
    showToast(message, type = 'info', title = '') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        toast.innerHTML = `
            <div class="toast-icon">
                <i class="${icons[type]}"></i>
            </div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
            <div class="toast-close">
                <i class="fas fa-times"></i>
            </div>
        `;
        
        container.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            this.removeToast(toast);
        }, 5000);
        
        // Close button
        toast.querySelector('.toast-close').addEventListener('click', () => {
            this.removeToast(toast);
        });
    }
    
    removeToast(toast) {
        gsap.to(toast, {
            duration: 0.3,
            x: 100,
            opacity: 0,
            ease: "power2.in",
            onComplete: () => {
                toast.remove();
            }
        });
    }
    
    async apiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (this.token) {
            options.headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        return fetch(`${this.apiBase}${endpoint}`, options);
    }
    
    logout() {
        localStorage.removeItem('token');
        this.token = null;
        this.currentUser = null;
        this.showLogin();
        this.showToast('Logged out successfully', 'info');
    }
}

// Global functions
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

function logout() {
    window.app.logout();
}

function showAddPatientModal() {
    window.app.showModal('addPatientModal');
}

function showPredictionModal() {
    window.app.showModal('predictionModal');
    window.predictionsManager.loadPatientsForSelect();
}

function showAddDoctorModal() {
    window.app.showModal('addDoctorModal');
}

function closeModal(modalId) {
    window.app.closeModal(modalId);
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});