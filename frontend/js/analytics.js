// Analytics Management

class AnalyticsManager {
    constructor(app) {
        this.app = app;
        this.charts = {};
    }
    
    async loadAnalytics() {
        try {
            this.app.showLoading();
            
            // Load all analytics data
            await Promise.all([
                this.loadRiskFactorsChart(),
                this.loadAgeDistributionChart(),
                this.loadCholesterolTrendsChart(),
                this.loadMonthlyPredictionsChart()
            ]);
            
        } catch (error) {
            console.error('Analytics error:', error);
            this.app.showToast('Error loading analytics', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    async loadRiskFactorsChart() {
        try {
            // For now, we'll create mock data
            // In a real app, you'd fetch this from the API
            const data = await this.getRiskFactorsData();
            this.createRiskFactorsChart(data);
        } catch (error) {
            console.error('Risk factors chart error:', error);
        }
    }
    
    async getRiskFactorsData() {
        // Mock data - in real app, fetch from API
        return {
            labels: ['High Cholesterol', 'High Blood Pressure', 'Diabetes', 'Smoking', 'Family History', 'Obesity'],
            values: [45, 38, 22, 15, 28, 33]
        };
    }
    
    createRiskFactorsChart(data) {
        const ctx = document.getElementById('riskFactorsChart');
        if (!ctx) return;
        
        if (this.charts.riskFactorsChart) {
            this.charts.riskFactorsChart.destroy();
        }
        
        this.charts.riskFactorsChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Risk Factor Prevalence (%)',
                    data: data.values,
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 50,
                        ticks: {
                            stepSize: 10
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    async loadAgeDistributionChart() {
        try {
            const data = await this.getAgeDistributionData();
            this.createAgeDistributionChart(data);
        } catch (error) {
            console.error('Age distribution chart error:', error);
        }
    }
    
    async getAgeDistributionData() {
        // Mock data - in real app, fetch from API
        return {
            labels: ['20-30', '31-40', '41-50', '51-60', '61-70', '71+'],
            lowRisk: [12, 18, 15, 8, 5, 2],
            highRisk: [3, 8, 12, 15, 18, 12]
        };
    }
    
    createAgeDistributionChart(data) {
        const ctx = document.getElementById('ageDistributionChart');
        if (!ctx) return;
        
        if (this.charts.ageDistributionChart) {
            this.charts.ageDistributionChart.destroy();
        }
        
        this.charts.ageDistributionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Low Risk',
                        data: data.lowRisk,
                        backgroundColor: 'rgba(76, 175, 80, 0.8)',
                        borderColor: 'rgba(76, 175, 80, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'High Risk',
                        data: data.highRisk,
                        backgroundColor: 'rgba(244, 67, 54, 0.8)',
                        borderColor: 'rgba(244, 67, 54, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Age Groups'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Number of Patients'
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    async loadCholesterolTrendsChart() {
        try {
            const data = await this.getCholesterolTrendsData();
            this.createCholesterolTrendsChart(data);
        } catch (error) {
            console.error('Cholesterol trends chart error:', error);
        }
    }
    
    async getCholesterolTrendsData() {
        // Mock data - in real app, fetch from API
        return {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            average: [220, 215, 218, 212, 208, 205],
            highRisk: [280, 275, 270, 268, 265, 262],
            lowRisk: [180, 175, 178, 172, 170, 168]
        };
    }
    
    createCholesterolTrendsChart(data) {
        const ctx = document.getElementById('cholesterolChart');
        if (!ctx) return;
        
        if (this.charts.cholesterolChart) {
            this.charts.cholesterolChart.destroy();
        }
        
        this.charts.cholesterolChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Average',
                        data: data.average,
                        borderColor: 'rgba(102, 126, 234, 1)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'High Risk Patients',
                        data: data.highRisk,
                        borderColor: 'rgba(244, 67, 54, 1)',
                        backgroundColor: 'rgba(244, 67, 54, 0.1)',
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Low Risk Patients',
                        data: data.lowRisk,
                        borderColor: 'rgba(76, 175, 80, 1)',
                        backgroundColor: 'rgba(76, 175, 80, 0.1)',
                        fill: false,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Cholesterol Level (mg/dl)'
                        },
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    async loadMonthlyPredictionsChart() {
        try {
            const response = await this.app.apiCall('/analytics/predictions-timeline', 'GET');
            if (response.ok) {
                const data = await response.json();
                this.createMonthlyPredictionsChart(data);
            }
        } catch (error) {
            console.error('Monthly predictions chart error:', error);
        }
    }
    
    createMonthlyPredictionsChart(data) {
        const ctx = document.getElementById('monthlyChart');
        if (!ctx) return;
        
        if (this.charts.monthlyChart) {
            this.charts.monthlyChart.destroy();
        }
        
        // Process data for monthly view
        const monthlyData = this.processMonthlyData(data);
        
        this.charts.monthlyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: monthlyData.labels,
                datasets: [{
                    label: 'Predictions',
                    data: monthlyData.values,
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Number of Predictions'
                        },
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    processMonthlyData(data) {
        // Group data by month
        const monthlyGroups = {};
        
        data.forEach(item => {
            const date = new Date(item.date);
            const monthKey = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;
            
            if (!monthlyGroups[monthKey]) {
                monthlyGroups[monthKey] = 0;
            }
            monthlyGroups[monthKey] += item.count;
        });
        
        // Convert to arrays
        const labels = Object.keys(monthlyGroups).map(key => {
            const [year, month] = key.split('-');
            const date = new Date(year, month - 1);
            return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        });
        
        const values = Object.values(monthlyGroups);
        
        return { labels, values };
    }
    
    // Export analytics data
    async exportAnalytics() {
        try {
            this.app.showLoading();
            
            // Gather all analytics data
            const analyticsData = {
                riskFactors: await this.getRiskFactorsData(),
                ageDistribution: await this.getAgeDistributionData(),
                cholesterolTrends: await this.getCholesterolTrendsData(),
                exportDate: new Date().toISOString()
            };
            
            // Create and download JSON file
            const dataStr = JSON.stringify(analyticsData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `heart_disease_analytics_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            this.app.showToast('Analytics data exported successfully', 'success');
            
        } catch (error) {
            console.error('Export error:', error);
            this.app.showToast('Error exporting analytics data', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    // Cleanup
    destroy() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {};
    }
}

// Initialize when app is ready
document.addEventListener('DOMContentLoaded', () => {
    window.analyticsManager = new AnalyticsManager(window.app);
});