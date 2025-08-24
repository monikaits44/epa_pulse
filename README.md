# ePA Pulse - Digital Health Dashboard

A comprehensive digital health management platform that combines Django REST API with Streamlit frontend to provide patients with personalized health insights, risk assessments, and medical recommendations.

## 🌟 Features

### Dashboard
- **Patient Overview**: Personalized health dashboard with key metrics
- **Health Alerts**: Real-time health alerts with risk assessments
- **Upcoming Appointments**: Schedule management and reminders
- **Data Upload**: CSV file upload functionality for patient data

### 🩺 Health Management
- **Test Results**: Comprehensive test result visualization and analysis
- **Medical History**: Track diagnoses, conditions, and medical records
- **Wearable Data Integration**: Real-time metrics from wearable devices
- **Insurance Policy Management**: Coverage details and policy information

### AI-Powered Features
- **Pulse Chatbot**: AI medical assistant for health-related queries
- **Risk Predictions**: Disease risk scoring using machine learning
- **Personalized Recommendations**: Custom health advice based on patient data
- **DiGA Watchlist**: Digital Health Application monitoring

### User Interface
- **Streamlit Frontend**: Modern, responsive web interface
- **Multi-page Application**: Organized into logical sections
- **Data Visualization**: Charts and graphs for health metrics
- **File Management**: Easy data upload and management

## 🏗️ Architecture

### Backend (Django)
- **REST API**: Django REST Framework for API endpoints
- **Database**: SQLite database for development
- **Models**: Patient, Policy, Appointment, TestResult, Prediction, Watchlist
- **AI Integration**: OpenAI API integration for medical insights

### Frontend (Streamlit)
- **Dashboard.py**: Main health dashboard
- **Test_Results.py**: Test results visualization
- **Pulse.py**: AI chatbot interface
- **Recommendations.py**: Health recommendations
- **Manage_my_data.py**: Data management interface

## 🛠️ Tech Stack

### Backend
- **Django 5.1.2**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database
- **OpenAI API**: AI-powered medical insights
- **Pandas**: Data manipulation
- **Python 3.12**: Programming language

### Frontend
- **Streamlit**: Web application framework
- **Pandas**: Data analysis
- **Matplotlib**: Data visualization
- **Requests**: HTTP client

### Data Sources
- **ePA Test Data**: Electronic Patient Act test datasets
- **DiGA Watchlist**: Digital Health Applications monitoring
- **AOK Bayern**: Health insurance data
- **myoncare**: Healthcare platform integration
- **gematik Specifications**: German health tech standards

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### 1. Clone the Repository
```bash
git clone <repository-url>
cd epa_pulse
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install django djangorestframework streamlit pandas matplotlib requests openai
```

### 4. Database Setup
```bash
cd epa_pulse
python manage.py makemigrations
python manage.py migrate
```

### 5. Populate Sample Data (Optional)
```bash
python manage.py populate_data
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
DJANGO_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
NVIDIA_API_KEY=your-nvidia-api-key
DEBUG=True
```

### API Configuration
Update the API URLs in the Streamlit files:
- Default API Base URL: `http://192.168.178.59:8000/api/`
- Update in `Dashboard.py`, `Test_Results.py`, `Pulse.py`, `Recommendations.py`

## Running the Application

### 1. Start Django Backend
```bash
cd epa_pulse
python manage.py runserver
```
The API will be available at `http://localhost:8000`

### 2. Start Streamlit Frontend
```bash
cd epa_pulse
streamlit run Dashboard.py
```
The frontend will be available at `http://localhost:8501`

## 📁 Project Structure

```
epa_pulse/
├── epa_pulse/              # Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── api/                   # Django app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # Data serializers
│   ├── urls.py            # API URLs
│   └── management/        # Custom commands
├── pages/                 # Streamlit pages
│   ├── Test_Results.py    # Test results page
│   ├── Pulse.py           # AI chatbot page
│   ├── Recommendations.py # Health recommendations
│   └── Manage_my_data.py  # Data management
├── data/                  # Sample datasets
│   ├── ePA Test Data/     # Electronic Patient Act data
│   ├── DiGA-Watchlist/    # Digital Health Apps
│   └── gematik-Spezifikationen/ # German health specs
├── Dashboard.py           # Main Streamlit app
├── manage.py             # Django management
└── db.sqlite3            # SQLite database
```

## API Endpoints

### Patient Data
- `GET /api/dashboard/{patient_id}/` - Patient dashboard data
- `POST /api/upload-patient-data/` - Upload patient data CSV

### Health Management
- `GET /api/policies/{patient_id}/` - Insurance policy information
- `GET /api/reminders/{patient_id}/` - Appointment reminders
- `GET /api/test-results/{patient_id}/` - Test results
- `GET /api/predictions/{patient_id}/` - Health predictions

### AI Features
- `POST /api/medical-bot/` - AI medical chatbot
- `GET /api/recommendations/{patient_id}/` - Health recommendations

## 🔒 Security Considerations

- Change the default Django secret key in production
- Set `DEBUG = False` in production
- Configure proper CORS settings
- Use environment variables for sensitive data
- Implement proper authentication and authorization

## 📊 Data Models

### Patient
- Personal information (name, age, gender, weight, height)
- Medical history (JSON field)
- Wearable data (JSON field)
- Linked insurance policy

### Policy
- Policy ID and coverage details
- Linked to patient

### TestResult
- Test type, date, result, and doctor information
- Linked to patient

### Appointment
- Date, type, status, and doctor
- Linked to patient

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **gematik**: For German healthcare digitalization standards
- **AOK Bayern**: For healthcare insurance data integration
- **DiGA Initiative**: For digital health application monitoring
- **OpenAI**: For AI-powered medical insights
- **Streamlit**: For the modern web framework

## Support

For support and questions, please open an issue in the GitHub repository.

---

**Note**: This is a proof-of-concept application for digital health management. Always consult with healthcare professionals for medical decisions.
