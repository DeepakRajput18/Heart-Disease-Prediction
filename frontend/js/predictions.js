// Predictions Management

class PredictionsManager {
    constructor(app) {
        this.app = app;
        this.predictions = [];
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Prediction form
        document.getElementById('predictionForm').addEventListener('submit', this.handlePrediction.bind(this));
    }
    
    async loadPredictions() {
        try {
            this.app.showLoading();
            
            // For now, we'll load all patients and their predictions
            // In a real app, you might want to paginate this
            const patientsResponse = await this.app.apiCall('/patients', 'GET');
            if (patientsResponse.ok) {
                const patients = await patientsResponse.json();
                await this.loadPredictionsForPatients(patients);
            }
            
        } catch (error) {
            console.error('Predictions error:', error);
            this.app.showToast('Error loading predictions', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    async loadPredictionsForPatients(patients) {
        const container = document.getElementById('predictionsContainer');
        container.innerHTML = '';
        
        for (const patient of patients) {
            try {
                const response = await this.app.apiCall(`/predictions/${patient.id}`, 'GET');
                if (response.ok) {
                    const predictions = await response.json();
                    if (predictions.length > 0) {
                        const patientCard = this.createPatientPredictionsCard(patient, predictions);
                        container.appendChild(patientCard);
                    }
                }
            } catch (error) {
                console.error(`Error loading predictions for patient ${patient.id}:`, error);
            }
        }
        
        // Animate cards
        gsap.from('.prediction-patient-card', {
            duration: 0.6,
            y: 30,
            opacity: 0,
            stagger: 0.1,
            ease: "power2.out"
        });
    }
    
    createPatientPredictionsCard(patient, predictions) {
        const card = document.createElement('div');
        card.className = 'prediction-patient-card';
        
        const latestPrediction = predictions[0]; // Assuming sorted by date desc
        const riskClass = latestPrediction.risk_level === 'High Risk' ? 'high-risk' : 'low-risk';
        
        card.innerHTML = `
            <div class="patient-card-header">
                <div class="patient-info">
                    <h3>${patient.name}</h3>
                    <p>${patient.email}</p>
                </div>
                <div class="risk-indicator ${riskClass}">
                    <i class="fas ${latestPrediction.risk_level === 'High Risk' ? 'fa-exclamation-triangle' : 'fa-check-circle'}"></i>
                    <span>${latestPrediction.risk_level}</span>
                </div>
            </div>
            
            <div class="predictions-timeline">
                <h4>Prediction History</h4>
                <div class="timeline">
                    ${predictions.map(prediction => this.createPredictionTimelineItem(prediction)).join('')}
                </div>
            </div>
            
            <div class="card-actions">
                <button class="btn btn-primary" onclick="window.predictionsManager.showPredictionModal('${patient.id}')">
                    <i class="fas fa-brain"></i>
                    New Prediction
                </button>
                <button class="btn btn-secondary" onclick="window.predictionsManager.viewPredictionDetails('${latestPrediction.id}')">
                    <i class="fas fa-eye"></i>
                    View Details
                </button>
            </div>
        `;
        
        return card;
    }
    
    createPredictionTimelineItem(prediction) {
        const date = new Date(prediction.created_at).toLocaleDateString();
        const riskClass = prediction.risk_level === 'High Risk' ? 'high-risk' : 'low-risk';
        const probability = (prediction.probability * 100).toFixed(1);
        
        return `
            <div class="timeline-item ${riskClass}">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <div class="timeline-header">
                        <span class="risk-label">${prediction.risk_level}</span>
                        <span class="date">${date}</span>
                    </div>
                    <div class="probability">
                        Risk Probability: ${probability}%
                    </div>
                </div>
            </div>
        `;
    }
    
    async loadPatientsForSelect() {
        try {
            const response = await this.app.apiCall('/patients', 'GET');
            if (response.ok) {
                const patients = await response.json();
                const select = document.getElementById('patientSelect');
                
                // Clear existing options except the first one
                select.innerHTML = '<option value="">Choose a patient...</option>';
                
                patients.forEach(patient => {
                    const option = document.createElement('option');
                    option.value = patient.id;
                    option.textContent = `${patient.name} (${patient.email})`;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading patients for select:', error);
        }
    }
    
    async handlePrediction(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const predictionData = {};
        
        for (let [key, value] of formData.entries()) {
            if (key === 'oldpeak') {
                predictionData[key] = parseFloat(value);
            } else if (key !== 'patient_id') {
                predictionData[key] = parseInt(value);
            } else {
                predictionData[key] = value;
            }
        }
        
        // Validate form
        if (!this.validatePredictionData(predictionData)) {
            return;
        }
        
        try {
            this.app.showLoading();
            
            const response = await this.app.apiCall('/predictions', 'POST', predictionData);
            
            if (response.ok) {
                const result = await response.json();
                
                this.app.closeModal('predictionModal');
                this.showPredictionResult(result);
                
                // Reload predictions
                this.loadPredictions();
                
                // Reset form
                e.target.reset();
                
            } else {
                const error = await response.json();
                this.app.showToast(error.detail || 'Error generating prediction', 'error');
            }
            
        } catch (error) {
            console.error('Prediction error:', error);
            this.app.showToast('Network error. Please try again.', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    validatePredictionData(data) {
        const required = [
            'patient_id', 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ];
        
        for (let field of required) {
            if (data[field] === undefined || data[field] === '' || data[field] === null) {
                this.app.showToast(`${field.replace('_', ' ')} is required`, 'error');
                return false;
            }
        }
        
        // Validate ranges
        if (data.age < 1 || data.age > 120) {
            this.app.showToast('Age must be between 1 and 120', 'error');
            return false;
        }
        
        if (data.trestbps < 80 || data.trestbps > 200) {
            this.app.showToast('Resting blood pressure must be between 80 and 200', 'error');
            return false;
        }
        
        if (data.chol < 100 || data.chol > 600) {
            this.app.showToast('Cholesterol must be between 100 and 600', 'error');
            return false;
        }
        
        if (data.thalach < 60 || data.thalach > 220) {
            this.app.showToast('Max heart rate must be between 60 and 220', 'error');
            return false;
        }
        
        return true;
    }
    
    showPredictionResult(result) {
        const modal = document.createElement('div');
        modal.id = 'predictionResultModal';
        modal.className = 'modal active';
        
        const probability = (result.probability * 100).toFixed(1);
        const riskClass = result.risk_level === 'High Risk' ? 'high-risk' : 'low-risk';
        
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Prediction Result</h2>
                    <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
                </div>
                
                <div class="prediction-result">
                    <div class="result-header ${riskClass}">
                        <div class="result-icon">
                            <i class="fas ${result.risk_level === 'High Risk' ? 'fa-exclamation-triangle' : 'fa-check-circle'}"></i>
                        </div>
                        <div class="result-info">
                            <h3>${result.risk_level}</h3>
                            <p>Risk Probability: ${probability}%</p>
                        </div>
                    </div>
                    
                    <div class="probability-bar">
                        <div class="probability-fill ${riskClass}" style="width: ${probability}%"></div>
                    </div>
                    
                    <div class="result-details">
                        <h4>Clinical Parameters Used:</h4>
                        <div class="parameters-grid">
                            <div class="parameter">
                                <label>Age:</label>
                                <span>${result.age} years</span>
                            </div>
                            <div class="parameter">
                                <label>Sex:</label>
                                <span>${result.sex === 1 ? 'Male' : 'Female'}</span>
                            </div>
                            <div class="parameter">
                                <label>Chest Pain Type:</label>
                                <span>${this.getChestPainType(result.cp)}</span>
                            </div>
                            <div class="parameter">
                                <label>Resting BP:</label>
                                <span>${result.trestbps} mm Hg</span>
                            </div>
                            <div class="parameter">
                                <label>Cholesterol:</label>
                                <span>${result.chol} mg/dl</span>
                            </div>
                            <div class="parameter">
                                <label>Max Heart Rate:</label>
                                <span>${result.thalach} bpm</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="result-recommendations">
                        <h4>Recommendations:</h4>
                        <ul>
                            ${this.getRecommendations(result).map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button class="btn btn-primary" onclick="this.closest('.modal').remove()">
                        <i class="fas fa-check"></i>
                        Close
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Animate modal and probability bar
        gsap.from(modal.querySelector('.modal-content'), {
            duration: 0.3,
            scale: 0.8,
            opacity: 0,
            ease: "back.out(1.7)"
        });
        
        gsap.to(modal.querySelector('.probability-fill'), {
            duration: 1.5,
            width: `${probability}%`,
            ease: "power2.out",
            delay: 0.5
        });
    }
    
    getChestPainType(cp) {
        const types = {
            0: 'Typical Angina',
            1: 'Atypical Angina',
            2: 'Non-anginal Pain',
            3: 'Asymptomatic'
        };
        return types[cp] || 'Unknown';
    }
    
    getRecommendations(result) {
        const recommendations = [];
        
        if (result.risk_level === 'High Risk') {
            recommendations.push('Consult with a cardiologist immediately');
            recommendations.push('Consider additional cardiac testing (ECG, stress test, echocardiogram)');
            recommendations.push('Monitor blood pressure and cholesterol levels regularly');
            recommendations.push('Implement lifestyle changes (diet, exercise, stress management)');
        } else {
            recommendations.push('Maintain regular check-ups with your healthcare provider');
            recommendations.push('Continue healthy lifestyle habits');
            recommendations.push('Monitor cardiovascular risk factors');
        }
        
        if (result.chol > 240) {
            recommendations.push('Consider cholesterol management strategies');
        }
        
        if (result.trestbps > 140) {
            recommendations.push('Monitor and manage blood pressure');
        }
        
        return recommendations;
    }
    
    showPredictionModal(patientId = null) {
        this.app.showModal('predictionModal');
        this.loadPatientsForSelect();
        
        if (patientId) {
            // Pre-select patient if provided
            setTimeout(() => {
                document.getElementById('patientSelect').value = patientId;
            }, 100);
        }
    }
    
    async viewPredictionDetails(predictionId) {
        // Implementation for viewing detailed prediction information
        this.app.showToast('Prediction details feature coming soon', 'info');
    }
}

// Initialize when app is ready
document.addEventListener('DOMContentLoaded', () => {
    window.predictionsManager = new PredictionsManager(window.app);
});