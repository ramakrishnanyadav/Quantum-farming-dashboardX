
# Deployment Instructions

## 🚀 Production Deployment Options

This guide covers deploying the Quantum Smart Farming Dashboard to various platforms, with **Streamlit Cloud** being the recommended and currently used solution.

## ☁️ Streamlit Cloud (Recommended - Currently Live)

### ✅ **Current Deployment**
Your app is successfully running at: https://quantum-farming-dashboard-9hmjhlbzsqdwhrfc5gfyug.streamlit.app/

### **Setup Steps**

#### 1. **Prepare Repository**
```bash
# Ensure these files are in your GitHub repo:
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # Documentation
```

#### 2. **Streamlit Configuration**
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

#### 3. **Deploy to Streamlit Cloud**
1. **Connect GitHub**: Link your repository to Streamlit Cloud
2. **Configure App**: 
   - **Repository**: `ramakrishnanyadav/quantum-farming-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. **Add Secrets**: In Streamlit Cloud dashboard
   ```
   OPENWEATHER_API_KEY = "your_api_key"
   ALPHA_VANTAGE_API_KEY = "your_api_key"
   ```
4. **Deploy**: Click "Deploy!" button

#### 4. **Post-Deployment Checklist**
- [ ] Test all quantum algorithms work
- [ ] Verify API integrations (weather data loading)
- [ ] Check quantum circuit visualizations
- [ ] Test parameter controls (qubits, layers, shots)
- [ ] Confirm Mumbai weather data displays correctly

## 🐳 Docker Deployment

### **Dockerfile**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Docker Compose**
```yaml
# docker-compose.yml
version: '3.8'

services:
  quantum-farming:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
      - ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### **Build and Run**
```bash
# Build image
docker build -t quantum-farming-dashboard .

# Run with environment file
docker run -p 8501:8501 --env-file .env quantum-farming-dashboard

# Or use Docker Compose
docker-compose up -d
```

## 🌐 Heroku Deployment

### **Setup Files**

#### Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### runtime.txt
```
python-3.9.18
```

### **Deployment Steps**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create quantum-farming-dashboard-app

# Set environment variables
heroku config:set OPENWEATHER_API_KEY=your_key
heroku config:set ALPHA_VANTAGE_API_KEY=your_key

# Deploy
git push heroku main

# Open app
heroku open
```

## ☁️ AWS Deployment

### **AWS App Runner**
```yaml
# apprunner.yaml
version: 1.0
runtime: python39
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  runtime-version: 3.9.18
  command: streamlit run app.py --server.port=8080 --server.address=0.0.0.0
  network:
    port: 8080
    env: PORT
  env:
    - name: OPENWEATHER_API_KEY
      value: your_api_key
    - name: ALPHA_VANTAGE_API_KEY  
      value: your_api_key
```

### **AWS ECS (Container)**
```json
{
  "family": "quantum-farming",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "quantum-farming-container",
      "image": "ramakrishnanyadav/quantum-farming:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENWEATHER_API_KEY",
          "value": "your_api_key"
        }
      ]
    }
  ]
}
```

## 🔧 Performance Optimization for Production

### **Quantum Circuit Optimization**
```python
# config/quantum_optimization.py
PRODUCTION_QUANTUM_CONFIG = {
    'max_qubits': 4,           # Limit for performance
    'max_circuit_depth': 3,    # Keep circuits shallow
    'default_shots': 1024,     # Balance accuracy vs speed
    'cache_quantum_results': True,
    'enable_circuit_caching': True
}
```

### **Streamlit Optimizations**
```python
# app.py optimizations
import streamlit as st

# Cache expensive operations
@st.cache_data(ttl=3600)  # 1 hour cache
def get_weather_data(lat, lon):
    return fetch_weather(lat, lon)

@st.cache_resource
def initialize_quantum_backend():
    return AerSimulator()

# Session state for quantum results
if 'quantum_results' not in st.session_state:
    st.session_state.quantum_results = {}
```

## 📊 Monitoring & Analytics

### **Application Monitoring**
```python
# monitoring/app_metrics.py
import streamlit as st
from datetime import datetime

def track_usage():
    """Track application usage metrics"""
    metrics = {
        'page_views': increment_counter('page_views'),
        'quantum_predictions': increment_counter('quantum_predictions'),
        'api_calls': increment_counter('api_calls'),
        'user_sessions': get_unique_sessions(),
        'last_deployment': get_deployment_timestamp()
    }
    return metrics
```

### **Health Checks**
```python
# health_check.py
def health_check():
    """Application health endpoint"""
    health = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'quantum_backend': check_quantum_backend(),
            'weather_api': check_weather_api(),
            'market_api': check_market_api()
        }
    }
    return health
```

## 🔐 Security Considerations

### **API Key Management**
- ✅ Use environment variables (never commit keys)
- ✅ Rotate API keys regularly
- ✅ Monitor API usage for anomalies
- ✅ Use minimal required permissions

### **Application Security**
```python
# security/validators.py
def validate_user_inputs(data):
    """Sanitize user inputs"""
    # Validate coordinate ranges
    if not (-90 <= data.get('lat', 0) <= 90):
        raise ValueError("Invalid latitude")
    
    # Validate quantum parameters
    if not (2 <= data.get('qubits', 0) <= 6):
        raise ValueError("Invalid qubit count")
    
    return sanitized_data
```

## 🚨 Rollback Procedures

### **Quick Rollback Steps**
```bash
# Streamlit Cloud
1. Go to Streamlit Cloud dashboard
2. Click "Reboot app" 
3. Or revert to previous GitHub commit

# Docker
docker pull yourusername/quantum-farming:previous-tag
docker stop quantum-farming
docker run -d --name quantum-farming ramakrishnanyadav/quantum-farming:previous-tag

# Heroku
heroku releases -a your-app-name
heroku rollback v123 -a your-app-name
```

## 📈 Scaling Considerations

### **Traffic Scaling**
- **Light Usage** (< 100 users/day):
