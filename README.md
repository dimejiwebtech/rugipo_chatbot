# RUGIPO Student Support Chatbot

A comprehensive AI-powered chatbot system designed to assist students at Rufus Giwa Polytechnic (RUGIPO) by providing quick access to information about the institution, particularly the Faculty of Engineering.

**Developer:** Oladimeji Shadrach Aliu

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## 🎯 Project Overview

The RUGIPO Student Support Chatbot is a full-stack web application built with Django and integrated with OpenAI's GPT-4o-mini model. It provides an intelligent conversational interface to help students navigate the institution, answer common questions about courses, programs, facilities, and administrative procedures.

The chatbot maintains conversation history, supports multiple concurrent sessions, and includes a fallback mechanism for when the OpenAI API is unavailable, ensuring the service remains accessible to students at all times.

## ✨ Features

### Core Functionality

- **AI-Powered Responses:** Integrates OpenAI's GPT-4o-mini model for intelligent, context-aware responses
- **Conversation Memory:** Maintains chat history per user session (last 10 messages for context)
- **Faculty of Engineering Knowledge Base:** Comprehensive Q&A database covering 5 engineering departments:
  - Agricultural and Bio-Environmental Engineering Technology (ABET)
  - Civil Engineering Technology (CET)
  - Computer Engineering Technology (CTE)
  - Electrical/Electronics Engineering Technology (EEET)
  - Mechanical Engineering Technology (MET)

### Robustness & Reliability

- **Fallback Search Mechanism:** Keyword-based search when OpenAI API is unavailable or quota exceeded
- **Session Management:** User sessions are stored and can be retrieved across multiple visits
- **Error Handling:** Graceful error handling with user-friendly messages

### User Experience

- **Chat Widget Interface:** Embedded chat widget on the website for easy access
- **Responsive Design:** Mobile-friendly interface using Tailwind CSS
- **Persistent Sessions:** Chat history and session ID stored in browser localStorage
- **Typing Indicator:** Visual feedback while awaiting bot response

### Website Pages

- **Home:** Welcome page with hero section and usage instructions
- **About:** Information about RUGIPO and the chatbot
- **Contact:** Contact form for student inquiries
- **Admin Interface:** Django admin panel for managing Q&A data and chat history

## 🛠️ Technology Stack

### Backend

- **Framework:** Django 5.2.7
- **Database:** SQLite (production-ready, can be migrated to PostgreSQL)
- **API Integration:** OpenAI Python SDK
- **Environment Management:** python-dotenv

### Frontend

- **Template Engine:** Django Templates
- **Styling:** Tailwind CSS 4.1.11
- **JavaScript:** Vanilla JavaScript (ES6 modules)
- **Build Tools:** Tailwind CLI

### Key Python Dependencies

- `django` - Web framework
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management

### Key JavaScript Dependencies

- `tailwindcss` - Utility-first CSS framework
- `autoprefixer` - PostCSS plugin for vendor prefixes
- `postcss` - CSS transformation tool

## 📁 Project Structure

```
rugipo_chatbot/
├── chatbot/                          # Main chatbot application
│   ├── migrations/                   # Database migrations
│   ├── services/
│   │   ├── __init__.py
│   │   └── openai_service.py        # OpenAI integration and fallback logic
│   ├── __init__.py
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py
│   ├── models.py                     # ChatSession, ChatMessage models
│   ├── tests.py
│   ├── urls.py                       # Chatbot URL routes
│   ├── views.py                      # Chat API endpoints
│   └── __pycache__/
│
├── config/                           # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                       # ASGI configuration
│   ├── settings.py                   # Project settings
│   ├── urls.py                       # Main URL configuration
│   ├── wsgi.py                       # WSGI configuration
│   └── __pycache__/
│
├── knowledge/                        # Knowledge management app
│   ├── migrations/                   # Database migrations
│   ├── __init__.py
│   ├── admin.py                      # Admin for Q&A management
│   ├── apps.py
│   ├── models.py                     # EngineeringQA model
│   ├── signals.py                    # Signals for data syncing
│   ├── tests.py
│   ├── utils.py                      # Utility functions
│   ├── views.py
│   └── __pycache__/
│
├── pages/                            # Website pages app
│   ├── migrations/                   # Database migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py                       # Pages URL routes
│   ├── views.py                      # Page views (home, about, contact)
│   └── __pycache__/
│
├── static/                           # Static files
│   ├── css/
│   │   ├── input.css                 # Tailwind input CSS
│   │   └── output.css                # Compiled Tailwind CSS
│   ├── images/                       # Image assets
│   ├── js/
│   │   ├── app.js                    # General app JavaScript
│   │   └── chatbot.js                # Chat widget JavaScript
│   └── videos/                       # Video assets
│
├── templates/                        # HTML templates
│   ├── base.html                     # Base template
│   ├── includes/
│   │   ├── chatbot_widget.html      # Chat widget component
│   │   ├── footer.html               # Footer component
│   │   └── navbar.html               # Navigation bar component
│   └── pages/
│       ├── about.html                # About page
│       ├── contact.html              # Contact page
│       └── home.html                 # Home page
│
├── data/
│   └── engineering_qa.json           # Engineering Q&A knowledge base (JSON export)
│
├── db.sqlite3                        # SQLite database
├── manage.py                         # Django management script
├── package.json                      # NPM configuration
└── test_api.py                       # API testing script
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Node.js 14+ (for Tailwind CSS)
- pip (Python package manager)
- npm (Node package manager)

### Step 1: Clone the Repository

```bash
cd c:\Users\Grimes\Desktop\rugipo_chatbot
```

### Step 2: Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or (Windows CMD)
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install django==5.2.7 openai python-dotenv
```

Or from requirements.txt (if available):

```bash
pip install -r requirements.txt
```

### Step 4: Install JavaScript Dependencies

```bash
npm install
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-django-secret-key-here
DEBUG=True
OPENAI_API_KEY=your-openai-api-key-here
KNOWLEDGE_BASE_JSON_PATH=data/engineering_qa.json
```

### Step 6: Run Database Migrations

```bash
python manage.py migrate
```

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### Step 8: Load Initial Data (Optional)

If you have initial Engineering Q&A data, load it via admin or use:

```bash
python manage.py loaddata initial_data
```

### Step 9: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## ⚙️ Configuration

### Django Settings

Key settings in `config/settings.py`:

- **DATABASES:** SQLite configured, can be changed to PostgreSQL
- **INSTALLED_APPS:** Includes pages, chatbot, and knowledge apps
- **TEMPLATES:** Django template engine configured
- **STATIC_URL:** Static files served from `/static/`

### OpenAI Configuration

The chatbot uses the following OpenAI settings (in `chatbot/services/openai_service.py`):

- **Model:** `gpt-4o-mini`
- **Temperature:** 0.7 (balanced creativity and consistency)
- **Max Tokens:** 500 (response length limit)

### Tailwind CSS Configuration

Build CSS:

```bash
npm run build
```

Watch mode for development:

```bash
npm run dev
```

## 📖 Usage

### Starting the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Accessing Admin Interface

Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

### Using the Chatbot

1. Navigate to the home page
2. Click the green chat button at the bottom right
3. Type your question about RUGIPO or the Faculty of Engineering
4. The chatbot will respond with relevant information

### Managing Q&A Data

In the Django admin panel:

1. Go to Knowledge → Engineering Q&As
2. Add, edit, or delete Q&A pairs
3. Select the appropriate engineering category
4. Add relevant keywords for better matching
5. Mark as active/inactive as needed

## 🔌 API Endpoints

### Chat API

All chat endpoints require JSON requests:

#### Send Message

**Endpoint:** `POST /chat/send-message/`

**Request Body:**

```json
{
  "message": "What are the core courses in Civil Engineering?",
  "session_id": "optional-uuid-or-empty"
}
```

**Response:**

```json
{
  "success": true,
  "bot_response": "Core courses include Structural Analysis...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Codes:**

- `200 OK` - Message sent successfully
- `400 Bad Request` - Missing message or session ID error

---

#### Get Chat History

**Endpoint:** `GET /chat/get-history/`

**Query Parameters:**

- `session_id` (required): UUID of the chat session

**Response:**

```json
{
  "success": true,
  "messages": [
    {
      "type": "user",
      "content": "What are the core courses in Civil Engineering?",
      "timestamp": "2025-12-04T10:30:00+00:00"
    },
    {
      "type": "bot",
      "content": "Core courses include...",
      "timestamp": "2025-12-04T10:30:05+00:00"
    }
  ]
}
```

**Status Codes:**

- `200 OK` - History retrieved successfully
- `400 Bad Request` - Session ID missing or invalid

---

### Web Pages

- `GET /` - Home page
- `GET /about/` - About page
- `GET /contact/` - Contact page
- `POST /contact/` - Submit contact form

## 💾 Database Models

### ChatSession

Stores individual chat sessions:

```python
- session_id: UUIDField (unique identifier)
- created_at: DateTimeField (creation timestamp)
- last_activity: DateTimeField (last message timestamp)
```

### ChatMessage

Stores individual chat messages:

```python
- session: ForeignKey (reference to ChatSession)
- message_type: CharField (choices: 'user' or 'bot')
- content: TextField (message content)
- created_at: DateTimeField (creation timestamp)
```

### EngineeringQA

Stores engineering department Q&A pairs:

```python
- category: CharField (5 engineering categories)
- question: TextField (the question)
- answer: TextField (the answer)
- keywords: CharField (comma-separated keywords)
- is_active: BooleanField (enable/disable Q&A)
- created_at: DateTimeField (creation timestamp)
- updated_at: DateTimeField (last update timestamp)
```

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable                   | Description                        | Example                    |
| -------------------------- | ---------------------------------- | -------------------------- |
| `SECRET_KEY`               | Django secret key for security     | `django-insecure-xyz...`   |
| `DEBUG`                    | Django debug mode                  | `True` or `False`          |
| `OPENAI_API_KEY`           | OpenAI API key for GPT integration | `sk-...`                   |
| `KNOWLEDGE_BASE_JSON_PATH` | Path to Q&A JSON file              | `data/engineering_qa.json` |

**Important:** Never commit `.env` file to version control. Add it to `.gitignore`.

## 🔧 Development

### Running Tests

```bash
python manage.py test
```

### Testing API with Python Script

A `test_api.py` script is available for testing the chatbot API:

```bash
python test_api.py
```

### Building Frontend Assets

Development (watch mode):

```bash
npm run dev
```

Production (minified):

```bash
npm run build
```

### Common Development Tasks

**Create a new Django app:**

```bash
python manage.py startapp app_name
```

**Make database migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Reset database:**

```bash
python manage.py flush
```

## 🐛 Troubleshooting

### Issue: "OpenAI API key is not configured"

**Solution:**

- Ensure `.env` file exists in project root
- Verify `OPENAI_API_KEY` is set correctly
- Restart the development server after updating `.env`

### Issue: "CSRF token missing or incorrect"

**Solution:**

- The `send-message/` endpoint has CSRF exemption for API access
- If using regular forms, ensure CSRF token is included: `{% csrf_token %}`

### Issue: Static files not loading (404 errors)

**Solution:**

```bash
python manage.py collectstatic --noinput
```

### Issue: "No module named 'openai'"

**Solution:**

```bash
pip install openai
```

### Issue: Chat messages not persisting

**Solution:**

- Ensure database migrations are applied: `python manage.py migrate`
- Check SQLite database file (`db.sqlite3`) exists and is readable
- Verify chat sessions table was created: `python manage.py dbshell`

### Issue: Tailwind CSS not compiling

**Solution:**

```bash
npm install
npm run build
```

### Issue: OpenAI API quota exceeded

**Solution:**

- The chatbot automatically switches to keyword-based fallback search
- Check OpenAI account usage and billing settings
- Consider upgrading your OpenAI plan

## 📊 Knowledge Base Structure

The Engineering Q&A knowledge base includes 5 categories:

1. **Agricultural and Bio-Environmental Engineering Technology (ABET)**
2. **Civil Engineering Technology (CET)**
3. **Computer Engineering Technology (CTE)**
4. **Electrical/Electronics Engineering Technology (EEET)**
5. **Mechanical Engineering Technology (MET)**

Each Q&A entry includes:

- Category classification
- Question text
- Answer text
- Searchable keywords
- Active/inactive status
- Timestamps for tracking

## 🎨 Frontend Components

### Chat Widget (`templates/includes/chatbot_widget.html`)

- Floating chat button at bottom-right
- Expandable chat window
- Message display area
- Input field with send button
- Typing indicator animation

### Base Template (`templates/base.html`)

- Navigation bar
- Chat widget inclusion
- Footer
- Static file management
- Block extension system for pages

### Styling

- Primary color: Green (#017C01) - RUGIPO theme
- Secondary colors: Yellow and Gray accents
- Responsive breakpoints for mobile and desktop
- Tailwind CSS utility classes throughout

## 📝 Notes

- The project uses Django's built-in admin interface for managing Q&A data
- Chat sessions are stored in the database for persistent history
- The fallback mechanism ensures service availability even without OpenAI access
- Browser localStorage is used to maintain session continuity across page reloads
- The chatbot system prompt is dynamically generated with current knowledge base data

## 🤝 Contributing

For improvements, bug fixes, or new features:

1. Test changes thoroughly in development mode
2. Update documentation accordingly
3. Follow Django and Python best practices
4. Ensure all migrations are included

## 📄 License

This project was developed by Oladimeji Shadrach Aliu for Rufus Giwa Polytechnic.

## 🆘 Support

For issues or questions:

- Check the troubleshooting section above
- Review Django documentation: https://docs.djangoproject.com/
- Check OpenAI documentation: https://platform.openai.com/docs/
- Contact the development team through the website contact form

---

**Last Updated:** December 4, 2025

**Current Version:** 1.0.0
