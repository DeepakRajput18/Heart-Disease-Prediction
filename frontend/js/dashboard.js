// Dashboard Management

class DashboardManager {
    constructor(app) {
        this.app = app;
        this.charts = {};
    }
    
    async loadDashboardData() {
        try {
            this.app.showLoading();
            
            // Load stats
            const statsResponse = await this.app.apiCall('/dashboard/stats', 'GET');
            if (statsResponse.ok) {
                const stats = await statsResponse.json();
                this.updateStats(stats);
            }
            
            // Load charts data
            await this.loadCharts();
            
        } catch (error) {
            console.error('Dashboard error:', error);
            this.app.showToast('Error loading dashboard', 'error');
        } finally {
            this.app.hideLoading();
        }
    }
    
    updateStats(stats) {
        // Update stat cards with animation
        this.animateStatUpdate('totalPatients', stats.total_patients);
        this.animateStatUpdate('highRiskPatients', stats.high_risk_patients);
        this.animateStatUpdate('recentPredictions', stats.recent_predictions);
        this.animateStatUpdate('totalPredictions', stats.total_predictions);
    }
    
    animateStatUpdate(elementId, targetValue) {
        const element = document.getElementById(elementId);
        const currentValue = parseInt(element.textContent) || 0;
        
        gsap.to({ value: currentValue }, {
            duration: 1.5,
            value: targetValue,
            ease: "power2.out",
            onUpdate: function() {
                element.textContent = Math.round(this.targets()[0].value);
            }
        });
    }
    
    async loadCharts() {
        try {
            // Risk distribution chart
            const riskResponse = await this.app.apiCall('/analytics/risk-distribution', 'GET');
            if (riskResponse.ok) {
                const riskData = await riskResponse.json();
                this.createRiskChart(riskData);
            }
            
            // Timeline chart
            const timelineResponse = await this.app.apiCall('/analytics/predictions-timeline', 'GET');
            if (timelineResponse.ok) {
                const timelineData = await timelineResponse.json();
                this.createTimelineChart(timelineData);
            }
            
        } catch (error) {
            console.error('Charts error:', error);
        }
    }
    
    createRiskChart(data) {
        const ctx = document.getElementById('riskChart');
        if (!ctx) return;
        
        // Destroy existing chart
        if (this.charts.riskChart) {
            this.charts.riskChart.destroy();
        }
        
        this.charts.riskChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.risk_level),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        'rgba(76, 175, 80, 0.8)',
                        'rgba(244, 67, 54, 0.8)',
                        'rgba(255, 193, 7, 0.8)'
                    ],
                    borderColor: [
                        'rgba(76, 175, 80, 1)',
                        'rgba(244, 67, 54, 1)',
                        'rgba(255, 193, 7, 1)'
                    ],
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 2000
                }
            }
        });
    }
    
    createTimelineChart(data) {
        const ctx = document.getElementById('timelineChart');
        if (!ctx) return;
        
        // Destroy existing chart
        if (this.charts.timelineChart) {
            this.charts.timelineChart.destroy();
        }
        
        // Process data for better visualization
        const processedData = this.processTimelineData(data);
        
        this.charts.timelineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: processedData.labels,
                datasets: [{
                    label: 'Predictions',
                    data: processedData.values,
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
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
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 1
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    processTimelineData(data) {
        // Sort data by date
        const sortedData = data.sort((a, b) => new Date(a.date) - new Date(b.date));
        
        // Format dates and extract values
        const labels = sortedData.map(item => {
            const date = new Date(item.date);
            return date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
            });
        });
        
        const values = sortedData.map(item => item.count);
        
        return { labels, values };
    }
    
    // Real-time updates
    startRealTimeUpdates() {
        // Update dashboard every 30 seconds
        this.updateInterval = setInterval(() => {
            this.loadDashboardData();
        }, 30000);
    }
    
    stopRealTimeUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
    
    // Cleanup
    destroy() {
        this.stopRealTimeUpdates();
        
        // Destroy all charts
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        
        this.charts = {};
    }
}

// Initialize when app is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardManager = new DashboardManager(window.app);
});