# 🫀 Heart Disease Prediction System

A comprehensive, production-ready web application for predicting heart disease risk using machine learning. Built with FastAPI, MongoDB, and modern web technologies.

## ✨ Features

### 🔐 Authentication & Security
- **JWT-based authentication** with secure login sessions
- **Role-based access control** (Admin/Doctor roles)
- **Password hashing** with bcrypt
- **Input validation** and sanitization
- **Audit logging** for all user actions
- **HTTPS support** with Nginx reverse proxy

### 👥 User Management
- **Doctor management** (Admin can add/remove doctors)
- **Multi-step patient registration** with validation
- **Patient CRUD operations** (Create, Read, Update, Delete)
- **Patient profile pages** with comprehensive information

### 🧠 Machine Learning
- **Heart disease prediction** using Logistic Regression
- **Clinical parameter input** with 13 medical features
- **Risk probability calculation** with confidence levels
- **Prediction history** and timeline tracking
- **Model performance metrics** and validation

### 📊 Analytics & Reporting
- **Interactive dashboard** with KPIs and statistics
- **Real-time charts** using Chart.js
- **Risk distribution analysis**
- **Prediction trends over time**
- **Age and cholesterol analytics**
- **Export functionality** for reports

### 📁 File Management
- **File upload system** for medical documents
- **ECG reports and images** storage
- **Patient document organization**
- **Secure file access** with authentication

### 🎨 Modern UI/UX
- **Responsive design** (Mobile + Desktop friendly)
- **Dark/Light theme toggle**
- **Smooth animations** with GSAP
- **Glassmorphism effects** and modern cards
- **Professional medical interface**
- **Toast notifications** and loading states

### 🐳 DevOps & Deployment
- **Docker containerization** for easy deployment
- **Docker Compose** for multi-service orchestration
- **MongoDB database** with proper indexing
- **Nginx reverse proxy** with rate limiting
- **Health checks** and monitoring
- **Environment configuration**

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB 4.4+
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd heart-disease-prediction
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize the database**
```bash
python init_db.py
```

5. **Start the application**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access the application**
- Open http://localhost:8000
- Login with: `admin@heartpredict.com` / `admin123`

### Docker Deployment

1. **Start with Docker Compose**
```bash
docker-compose up -d
```

2. **Initialize the database**
```bash
docker-compose exec backend python init_db.py
```

3. **Access the application**
- Open http://localhost
- Login with default credentials

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py              # FastAPI application
├── auth.py              # Authentication & JWT
├── database.py          # MongoDB connection
├── models.py            # Pydantic models
├── ml_model.py          # Machine learning model
└── utils.py             # Utility functions
```

### Frontend (Vanilla JS)
```
frontend/
├── index.html           # Main HTML file
├── css/
│   ├── styles.css       # Main styles
│   └── animations.css   # Animation styles
└── js/
    ├── app.js           # Main application
    ├── auth.js          # Authentication
    ├── dashboard.js     # Dashboard management
    ├── patients.js      # Patient management
    ├── predictions.js   # Prediction system
    ├── analytics.js     # Analytics & charts
    └── utils.js         # Utility functions
```

### Database Schema
- **doctors**: User accounts and authentication
- **patients**: Patient information and medical history
- **predictions**: ML predictions and results
- **audit_logs**: System activity tracking
- **files**: Uploaded documents and references

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_auth.py -v
```

### Test Coverage
- Authentication and authorization
- Patient CRUD operations
- Prediction model accuracy
- API endpoint validation
- Database operations

## 📊 Machine Learning Model

### Features Used
1. **Age** - Patient age in years
2. **Sex** - Gender (1 = male, 0 = female)
3. **CP** - Chest pain type (0-3)
4. **Trestbps** - Resting blood pressure (mm Hg)
5. **Chol** - Serum cholesterol (mg/dl)
6. **FBS** - Fasting blood sugar > 120 mg/dl
7. **Restecg** - Resting ECG results (0-2)
8. **Thalach** - Maximum heart rate achieved
9. **Exang** - Exercise induced angina
10. **Oldpeak** - ST depression induced by exercise
11. **Slope** - Slope of peak exercise ST segment
12. **CA** - Number of major vessels (0-3)
13. **Thal** - Thalassemia type (0-2)

### Model Performance
- **Algorithm**: Logistic Regression
- **Training Accuracy**: ~85%
- **Testing Accuracy**: ~82%
- **Cross-validation**: 5-fold CV implemented

## 🔧 Configuration

### Environment Variables
```bash
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=heart_disease_db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Docker Configuration
- **Backend**: Python 3.11 with FastAPI
- **Database**: MongoDB 7.0
- **Proxy**: Nginx with SSL support
- **Volumes**: Persistent data storage

## 🛡️ Security Features

### Authentication
- JWT tokens with expiration
- Password hashing with bcrypt
- Secure session management
- Role-based access control

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection headers
- CSRF protection
- Rate limiting

### Infrastructure
- HTTPS encryption
- Secure headers
- Database connection security
- File upload restrictions

## 📈 Monitoring & Logging

### Audit Logs
- User login/logout events
- Patient data modifications
- Prediction generations
- File uploads/downloads
- Administrative actions

### Health Checks
- Application health endpoint
- Database connectivity
- Model availability
- System resource monitoring

## 🚀 Deployment Options

### Cloud Platforms
- **AWS**: ECS, RDS, S3
- **Google Cloud**: Cloud Run, Cloud SQL
- **Azure**: Container Instances, CosmosDB
- **DigitalOcean**: App Platform, Managed Databases

### On-Premise
- Docker Swarm
- Kubernetes
- Traditional server deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test cases for examples

## 🔮 Future Enhancements

- [ ] Advanced ML models (Random Forest, Neural Networks)
- [ ] Real-time notifications
- [ ] Mobile app development
- [ ] Integration with medical devices
- [ ] Telemedicine features
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] AI-powered recommendations

---

**⚠️ Medical Disclaimer**: This application is for educational and demonstration purposes only. It should not be used for actual medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals for medical advice.