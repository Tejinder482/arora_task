# Medical Message Classification System

A Django-based web application that uses AI to automatically classify patient medical messages into different priority categories. This system helps healthcare providers triage patient communications efficiently by categorizing them as emergency, routine, follow-up, or other types of messages.

## 🚀 Features

- **AI-Powered Classification**: Uses Ollama with the DeepSeek-R1 model to intelligently categorize medical messages
- **Real-time Processing**: Instant message classification with confidence scores
- **Patient History**: Tracks and displays previous messages from the same patient
- **RESTful API**: JSON API endpoints for integration with other systems
- **Web Interface**: User-friendly web form for message submission
- **Category System**: Classifies messages into four categories:
  - **Emergency**: Life-threatening situations requiring immediate attention
  - **Routine**: Normal medical care that can wait
  - **Follow-up**: Messages about previous treatments or appointments
  - **Other**: Non-medical or administrative messages

## 🛠️ Technology Stack

- **Backend**: Django 4.x with Django REST Framework
- **Database**: SQLite (default, easily configurable to PostgreSQL/MySQL)
- **AI Model**: DeepSeek-R1 via Ollama API
- **Frontend**: HTML/CSS/JavaScript
- **API**: RESTful JSON endpoints

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- DeepSeek-R1 model downloaded in Ollama

### Installing Ollama and DeepSeek-R1

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Pull the DeepSeek-R1 model:
   ```bash
   ollama pull deepseek-r1:latest
   ```
3. Start Ollama service:
   ```bash
   ollama serve
   ```

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aroraTask
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   
   # On Windows
   myenv\Scripts\activate
   
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install django
   pip install djangorestframework
   pip install drf-yasg
   pip install requests
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## 📖 Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Fill out the form with:
   - Patient name
   - Mobile number
   - Medical message
3. Submit the form to get instant AI classification
4. View previous messages from the same patient

### API Endpoints

#### API Overview

**GET** `/api/`

Get information about available API endpoints and documentation links.

**Response:**
```json
{
    "message": "Medical Message Classification API",
    "version": "v1.0.0",
    "description": "AI-powered medical message classification using DeepSeek-R1 model",
    "endpoints": {
        "submit_message": "/submit-message/ (POST)",
        "swagger_ui": "/swagger/",
        "redoc": "/redoc/",
        "api_overview": "/api/"
    },
    "categories": ["emergency", "routine", "followup", "other"]
}
```

#### Submit Message for Classification

**POST** `/submit-message/`

**Request Body:**
```json
{
    "name": "John Doe",
    "mobile": "+1234567890",
    "message": "I have severe chest pain and difficulty breathing"
}
```

**Response:**
```json
{
    "success": true,
    "current_result": {
        "category": "emergency",
        "confidence": 0.95
    },
    "history": [
        {
            "message": "Previous message",
            "category": "routine",
            "confidence": 0.87,
            "timestamp": "2024-01-15 10:30"
        }
    ],
    "ai_response": "emergency\n95%",
    "timestamp": "14:25"
}
```

## 🗃️ Database Schema

### PatientMessage Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `name` | CharField(200) | Patient name |
| `mobile` | CharField(20) | Patient mobile number (indexed) |
| `message` | TextField | Medical message content |
| `category` | CharField(20) | AI-classified category |
| `confidence` | FloatField | AI confidence score (0.0-1.0) |
| `created_at` | DateTimeField | Timestamp of message submission |

## 🔧 Configuration

### AI Model Configuration

The AI model can be configured in `MainApp/aimodel.py`:

```python
def generate_response(message, model="deepseek-r1:latest"):
    # Change model parameter to use different Ollama models
```

### Category Definitions

Categories are defined in the AI prompt and can be modified in `MainApp/aimodel.py`:

- **Emergency**: Life-threatening, needs immediate help
- **Routine**: Normal medical care, can wait
- **Follow-up**: About previous treatment or appointment
- **Other**: Not medical or administrative

## 🚨 Troubleshooting

### Common Issues

1. **"Could not connect to Ollama"**
   - Ensure Ollama is running: `ollama serve`
   - Check if DeepSeek-R1 model is installed: `ollama list`

2. **AI Response Parsing Errors**
   - The system falls back to "other" category with 50% confidence
   - Check Ollama logs for model response issues

3. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Check if SQLite database file has proper permissions

## 📚 API Documentation

This application includes comprehensive API documentation using Swagger/OpenAPI:

### Documentation URLs

- **Swagger UI**: `http://localhost:8000/swagger/` - Interactive API documentation
- **ReDoc**: `http://localhost:8000/redoc/` - Alternative documentation format  
- **OpenAPI Schema**: `http://localhost:8000/swagger.json` - Raw OpenAPI schema
- **API Overview**: `http://localhost:8000/api/` - Quick endpoint reference

### Features of the Documentation

- **Interactive Testing**: Try out API endpoints directly from the Swagger UI
- **Request/Response Examples**: See example requests and responses for all endpoints
- **Schema Validation**: View detailed input validation requirements
- **Error Handling**: Documentation of all possible error responses
- **Model Definitions**: Complete data structure documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Ensure all prerequisites are properly installed

## 🔄 Version History

- **v1.0.0**: Initial release with basic AI classification functionality
  - Django web interface
  - RESTful API
  - Patient message history
  - Ollama integration with DeepSeek-R1

---

**Note**: This application is designed for demonstration purposes. For production use in healthcare environments, ensure compliance with relevant regulations like HIPAA and implement appropriate security measures. 