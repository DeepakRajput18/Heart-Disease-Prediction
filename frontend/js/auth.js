// Authentication Management

class AuthManager {
    constructor(app) {
        this.app = app;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Login form
        document.getElementById('loginForm').addEventListener('submit', this.handleLogin.bind(this));
    }
    
    async handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        if (!email || !password) {
            this.app.showToast('Please fill in all fields', 'error');
            return;
        }
        
        try {
            this.app.showLoading();
            
            const response = await this.app.apiCall('/auth/login', 'POST', {
                email,
                password
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Store token and user info
                localStorage.setItem('token', data.access_token);
                this.app.token = data.access_token;
                this.app.currentUser = data.doctor_info;
                
                // Update UI with user info
                this.updateUserInfo(data.doctor_info);
                
                // Show dashboard
                this.app.showDashboard();
                
                this.app.showToast('Login successful!', 'success', 'Welcome back');
                
                // Clear form
                document.getElementById('loginForm').reset();
                
            } else {
                const error = await response.json();
                this.app.showToast(error.detail || 'Login failed', 'error');
                
                // Shake animation for error
                gsap.to('.login-card', {
                    duration: 0.1,
                    x: -10,
                    yoyo: true,
                    repeat: 5,
                    ease: "power2.inOut"
                });
            }
            
        } catch (error) {
            console.error('Login error:', error);
            this.app.showToast('Network error. Please try again.', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    updateUserInfo(doctorInfo) {
        document.getElementById('userName').textContent = doctorInfo.name;
        document.getElementById('userRole').textContent = doctorInfo.specialization;
        
        // Show/hide admin features
        if (doctorInfo.role === 'admin') {
            document.getElementById('doctorsNav').style.display = 'block';
        } else {
            document.getElementById('doctorsNav').style.display = 'none';
        }
    }
    
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    validatePassword(password) {
        return password.length >= 6;
    }
}

// Initialize when app is ready
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager(window.app);
});