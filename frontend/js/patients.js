// Patient Management

class PatientsManager {
    constructor(app) {
        this.app = app;
        this.patients = [];
        this.currentStep = 1;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Add patient form
        document.getElementById('addPatientForm').addEventListener('submit', this.handleAddPatient.bind(this));
    }
    
    async loadPatients() {
        try {
            this.app.showLoading();
            
            const response = await this.app.apiCall('/patients', 'GET');
            if (response.ok) {
                this.patients = await response.json();
                this.displayPatients();
            } else {
                this.app.showToast('Error loading patients', 'error');
            }
            
        } catch (error) {
            console.error('Patients error:', error);
            this.app.showToast('Network error loading patients', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    displayPatients() {
        const tbody = document.getElementById('patientsTableBody');
        tbody.innerHTML = '';
        
        this.patients.forEach((patient, index) => {
            const row = this.createPatientRow(patient, index);
            tbody.appendChild(row);
        });
        
        // Animate rows
        gsap.from('#patientsTableBody tr', {
            duration: 0.5,
            y: 20,
            opacity: 0,
            stagger: 0.1,
            ease: "power2.out"
        });
    }
    
    createPatientRow(patient, index) {
        const row = document.createElement('tr');
        row.className = 'patient-row';
        
        const age = this.calculateAge(patient.date_of_birth);
        
        row.innerHTML = `
            <td>
                <div class="patient-name">
                    <strong>${patient.name}</strong>
                </div>
            </td>
            <td>${patient.email}</td>
            <td>${patient.phone}</td>
            <td>${age}</td>
            <td>
                <span class="gender-badge ${patient.gender}">
                    ${patient.gender.charAt(0).toUpperCase() + patient.gender.slice(1)}
                </span>
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn-icon" onclick="window.patientsManager.viewPatient('${patient.id}')" title="View">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn-icon" onclick="window.patientsManager.editPatient('${patient.id}')" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-icon danger" onclick="window.patientsManager.deletePatient('${patient.id}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        
        return row;
    }
    
    calculateAge(dateOfBirth) {
        const today = new Date();
        const birthDate = new Date(dateOfBirth);
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        
        return age;
    }
    
    async handleAddPatient(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const patientData = {};
        
        for (let [key, value] of formData.entries()) {
            patientData[key] = value;
        }
        
        // Validate required fields
        if (!this.validatePatientData(patientData)) {
            return;
        }
        
        try {
            this.app.showLoading();
            
            const response = await this.app.apiCall('/patients', 'POST', patientData);
            
            if (response.ok) {
                const newPatient = await response.json();
                this.patients.unshift(newPatient);
                this.displayPatients();
                
                this.app.closeModal('addPatientModal');
                this.app.showToast('Patient added successfully!', 'success');
                
                // Reset form
                e.target.reset();
                this.resetMultiStepForm();
                
            } else {
                const error = await response.json();
                this.app.showToast(error.detail || 'Error adding patient', 'error');
            }
            
        } catch (error) {
            console.error('Add patient error:', error);
            this.app.showToast('Network error. Please try again.', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    validatePatientData(data) {
        const required = ['name', 'email', 'phone', 'date_of_birth', 'gender', 'address', 'emergency_contact'];
        
        for (let field of required) {
            if (!data[field] || data[field].trim() === '') {
                this.app.showToast(`${field.replace('_', ' ')} is required`, 'error');
                return false;
            }
        }
        
        // Validate email
        if (!this.validateEmail(data.email)) {
            this.app.showToast('Please enter a valid email address', 'error');
            return false;
        }
        
        // Validate date of birth
        const birthDate = new Date(data.date_of_birth);
        const today = new Date();
        if (birthDate >= today) {
            this.app.showToast('Date of birth must be in the past', 'error');
            return false;
        }
        
        return true;
    }
    
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    async viewPatient(patientId) {
        const patient = this.patients.find(p => p.id === patientId);
        if (!patient) return;
        
        // Create and show patient details modal
        this.showPatientDetailsModal(patient);
    }
    
    showPatientDetailsModal(patient) {
        // Create modal dynamically
        const modal = document.createElement('div');
        modal.id = 'patientDetailsModal';
        modal.className = 'modal active';
        
        const age = this.calculateAge(patient.date_of_birth);
        
        modal.innerHTML = `
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>Patient Details</h2>
                    <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
                </div>
                
                <div class="patient-details-content">
                    <div class="patient-header">
                        <div class="patient-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="patient-info">
                            <h3>${patient.name}</h3>
                            <p>${age} years old • ${patient.gender}</p>
                        </div>
                    </div>
                    
                    <div class="details-grid">
                        <div class="detail-section">
                            <h4>Contact Information</h4>
                            <div class="detail-item">
                                <i class="fas fa-envelope"></i>
                                <span>${patient.email}</span>
                            </div>
                            <div class="detail-item">
                                <i class="fas fa-phone"></i>
                                <span>${patient.phone}</span>
                            </div>
                            <div class="detail-item">
                                <i class="fas fa-map-marker-alt"></i>
                                <span>${patient.address}</span>
                            </div>
                        </div>
                        
                        <div class="detail-section">
                            <h4>Emergency Contact</h4>
                            <div class="detail-item">
                                <i class="fas fa-user-friends"></i>
                                <span>${patient.emergency_contact}</span>
                            </div>
                        </div>
                        
                        <div class="detail-section">
                            <h4>Medical History</h4>
                            <div class="medical-history">
                                ${patient.medical_history || 'No medical history recorded'}
                            </div>
                        </div>
                    </div>
                    
                    <div class="patient-actions">
                        <button class="btn btn-primary" onclick="window.patientsManager.editPatient('${patient.id}')">
                            <i class="fas fa-edit"></i>
                            Edit Patient
                        </button>
                        <button class="btn btn-secondary" onclick="window.predictionsManager.showPredictionModal('${patient.id}')">
                            <i class="fas fa-brain"></i>
                            New Prediction
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Animate modal
        gsap.from(modal.querySelector('.modal-content'), {
            duration: 0.3,
            scale: 0.8,
            opacity: 0,
            ease: "back.out(1.7)"
        });
    }
    
    async editPatient(patientId) {
        // Implementation for editing patient
        this.app.showToast('Edit patient feature coming soon', 'info');
    }
    
    async deletePatient(patientId) {
        if (!confirm('Are you sure you want to delete this patient? This action cannot be undone.')) {
            return;
        }
        
        try {
            this.app.showLoading();
            
            const response = await this.app.apiCall(`/patients/${patientId}`, 'DELETE');
            
            if (response.ok) {
                this.patients = this.patients.filter(p => p.id !== patientId);
                this.displayPatients();
                this.app.showToast('Patient deleted successfully', 'success');
            } else {
                this.app.showToast('Error deleting patient', 'error');
            }
            
        } catch (error) {
            console.error('Delete patient error:', error);
            this.app.showToast('Network error. Please try again.', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    // Multi-step form methods
    changeStep(direction) {
        const steps = document.querySelectorAll('.step');
        const totalSteps = steps.length;
        
        // Hide current step
        steps[this.currentStep - 1].classList.remove('active');
        
        // Update step
        this.currentStep += direction;
        
        // Show new step
        steps[this.currentStep - 1].classList.add('active');
        
        // Update navigation buttons
        this.updateStepNavigation();
        
        // Animate step transition
        gsap.from(steps[this.currentStep - 1], {
            duration: 0.3,
            x: direction > 0 ? 50 : -50,
            opacity: 0,
            ease: "power2.out"
        });
    }
    
    updateStepNavigation() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');
        
        // Show/hide previous button
        prevBtn.style.display = this.currentStep === 1 ? 'none' : 'inline-flex';
        
        // Show/hide next/submit buttons
        if (this.currentStep === 2) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }
    }
    
    resetMultiStepForm() {
        this.currentStep = 1;
        
        // Reset steps
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.toggle('active', index === 0);
        });
        
        // Reset navigation
        this.updateStepNavigation();
    }
}

// Global functions for multi-step form
function changeStep(direction) {
    window.patientsManager.changeStep(direction);
}

// Initialize when app is ready
document.addEventListener('DOMContentLoaded', () => {
    window.patientsManager = new PatientsManager(window.app);
});