# Employee Mood Check Module

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Key Components](#key-components)
4. [Workflow](#workflow)
5. [Database Models](#database-models)
6. [API Endpoints](#api-endpoints)
7. [Setup & Configuration](#setup--configuration)
8. [Usage Examples](#usage-examples)
9. [Dependencies](#dependencies)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The **Employee Mood Check Module** is a Flask-based application designed to collect, track, and analyze employee mood data through WhatsApp interactions. The system enables organizations to:

- **Collect Mood Ratings**: Employees can rate their mood on a scale of 1-4 (Great, Good, Okay, Not so good)
- **Gather Feedback**: For negative ratings, the system automatically asks for detailed feedback
- **AI-Powered Responses**: Uses AI to generate professional HR-like acknowledgment responses
- **Analytics & Reporting**: Provides comprehensive statistics and analytics on employee mood trends
- **Session Management**: Maintains conversation context during mood check interactions

### Key Features
- ✅ WhatsApp-based mood collection
- ✅ AI-generated professional responses
- ✅ Session-based conversation management
- ✅ Comprehensive mood analytics and statistics
- ✅ Employee risk identification
- ✅ Date-wise and employee-wise mood tracking
- ✅ Integration with existing employee management system

---

## Architecture

The module follows a **layered architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         API Layer (api.py)              │
│     - REST API Endpoints                │
│     - Request Validation                │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│    Business Logic (employee_mood_check) │
│     - Main workflow orchestration        │
│     - AI agent integration               │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│      Proxy Layer (proxies/)              │
│     - Abstraction layer                  │
│     - Session management                 │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│      Service Layer (services/)           │
│     - Business logic implementation      │
│     - Database operations                │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│      Database Layer (SQLAlchemy)         │
│     - Data models                        │
│     - Database connections               │
└─────────────────────────────────────────┘
```

### Directory Structure

```
Employee Mood Module/
├── app.py                          # Flask application initialization
├── api.py                          # API endpoints
├── database.py                     # Database configuration
├── employee_mood_check.py          # Main mood check workflow
├── Files/
│   └── SQLAlchemyModels.py         # Database models
├── proxies/                        # Proxy layer (abstraction)
│   ├── employee_mood_proxy.py
│   ├── employee_mood_session_proxy.py
│   ├── employee_session_proxy.py
│   ├── employee_message_proxy.py
│   └── ...
├── services/                       # Service layer (business logic)
│   ├── employee_mood_service.py
│   ├── employee_mood_session_service.py
│   └── ...
├── helpers/                        # Helper utilities
│   ├── contact_validation.py
│   ├── email_validation.py
│   └── ...
└── utils/                          # Utility functions
    ├── agents.py                   # AI agent functions
    ├── ai_client.py                # AI client configuration
    └── formats.py                  # Data format models
```

---

## Key Components

### 1. **Main Workflow** (`employee_mood_check.py`)

The core function `employee_mood_check()` orchestrates the entire mood check process:

**Function Signature:**
```python
def employee_mood_check(contact_number: str, user_message: str, mood_record_id: int = None)
```

**Responsibilities:**
- Identifies employee by contact number
- Manages conversation flow (first-time vs. follow-up)
- Sends follow-up questions for negative ratings
- Records user feedback
- Generates AI-powered responses
- Updates mood records with comments
- Cleans up session data after completion

### 2. **AI Agents** (`utils/agents.py`)

**`mood_check_response(message: str)`**
- Generates professional HR-like acknowledgment responses
- Uses GPT model to create contextually appropriate replies
- Returns structured response in `MoodCheckResponse` format

**`get_employee_mood_check_extraction(messages: list)`**
- Extracts structured data from employee feedback
- Parses comments and reasons from conversation history

### 3. **Session Management** (`proxies/employee_mood_session_proxy.py`)

Manages conversation state during mood check interactions:

- **`set_employee_asked_user_feedback()`**: Marks that feedback question was asked
- **`get_employee_asked_user_feedback()`**: Checks if feedback was already requested
- **`clear_employee_asked_user_feedback()`**: Resets feedback flag after completion

### 4. **Mood Service** (`services/employee_mood_service.py`)

Handles all mood-related database operations:

- **`add_comment_to_mood_record_by_id()`**: Adds comments to existing mood records
- **`get_mood_check_statistics()`**: Generates comprehensive analytics including:
  - Mood distribution (counts and percentages)
  - Statistical analysis (mean, median, mode, std deviation)
  - Trend analysis (improving/worsening/stable)
  - Employee risk identification
  - Date-wise and employee-wise breakdowns

### 5. **Message History** (`proxies/employee_message_proxy.py`)

Tracks all conversation messages for audit and context:

- **`save_message()`**: Stores messages with role (user/assistant) and timestamp
- **`get_message_history()`**: Retrieves conversation history
- **`clear_message_history()`**: Cleans up old messages

---

## Workflow

### Mood Check Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Employee submits mood rating (1-4)                       │
│    - 1 = Great, 2 = Good, 3 = Okay, 4 = Not so good        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. System checks if rating is negative (3 or 4)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
    Negative (3,4)              Positive (1,2)
         │                           │
         │                           └──► End (No follow-up)
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Check if feedback already requested                      │
│    (EmployeeMoodSessionProxy.get_employee_asked_user_feedback)│
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
    Not Asked Yet              Already Asked
         │                           │
         │                           ▼
         │              ┌────────────────────────────────────┐
         │              │ 4. User provides feedback message   │
         │              └────────────────────────────────────┘
         │                           │
         │                           ▼
         │              ┌────────────────────────────────────┐
         │              │ 5. Save message to history         │
         │              └────────────────────────────────────┘
         │                           │
         │                           ▼
         │              ┌────────────────────────────────────┐
         │              │ 6. Update mood record with comment  │
         │              └────────────────────────────────────┘
         │                           │
         │                           ▼
         │              ┌────────────────────────────────────┐
         │              │ 7. Generate AI response            │
         │              │    (mood_check_response)           │
         │              └────────────────────────────────────┘
         │                           │
         │                           ▼
         │              ┌────────────────────────────────────┐
         │              │ 8. Send response to employee      │
         │              └────────────────────────────────────┘
         │                           │
         │                           ▼
         │              ┌────────────────────────────────────┐
         │              │ 9. Clear session data              │
         │              └────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Send follow-up question:                                 │
│    "Thank you so much for your feedback.                    │
│     May I know what made you feel that way?"                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Set feedback flag to True                                │
│    (EmployeeMoodSessionProxy.set_employee_asked_user_feedback)│
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process

1. **Initialization**
   - Employee submits mood rating through WhatsApp
   - System identifies employee by contact number
   - Mood record is created in database

2. **Negative Rating Detection**
   - If rating is 3 (Okay) or 4 (Not so good), system triggers follow-up

3. **First Interaction (Feedback Request)**
   - System checks if feedback question was already asked
   - If not asked: Sends follow-up question
   - Sets `asked_user_feedback` flag to `True`
   - Saves message to history

4. **Second Interaction (Feedback Collection)**
   - Employee responds with feedback
   - System saves message to history
   - Updates mood record with comment (if `mood_record_id` provided)
   - Loads conversation context

5. **AI Response Generation**
   - Calls `mood_check_response()` with user's feedback
   - AI generates professional HR acknowledgment
   - Response is sent to employee via WhatsApp

6. **Session Cleanup**
   - Clears session messages
   - Resets `asked_user_feedback` flag
   - Conversation ends

---

## Database Models

### MoodCheck Model

The primary model for storing mood data:

```python
class MoodCheck(db.Model):
    __tablename__ = "mood_checks"
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey("employee.id"))
    company_id = db.Column(db.Integer, ForeignKey("companies.id"))
    mood = db.Column(db.Enum('1', '2', '3', '4'))  # 1=Great, 2=Good, 3=Okay, 4=Not so good
    comments = db.Column(db.Text, nullable=True)    # Employee feedback
    checked_at = db.Column(db.DateTime)             # Timestamp
    date = db.Column(db.Date)                       # Date of mood check
```

### SessionState Model

Stores conversation state and session data:

```python
class SessionState(db.Model):
    __tablename__ = 'session_state'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_number = db.Column(db.String)
    session_key = db.Column(db.String)      # e.g., 'employee_asked_user_feedback'
    session_value = db.Column(db.String)    # Value stored as string
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
```

### LeadMessageHistory Model

Tracks all conversation messages:

```python
class LeadMessageHistory(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True)
    contact_number = db.Column(db.String)
    role = db.Column(db.String)             # 'user' or 'assistant'
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
```

---

## API Endpoints

The module includes several API endpoints (defined in `api.py`), though the mood check functionality is primarily triggered through WhatsApp interactions. Key endpoints include:

### Employee Management APIs

- **`POST /crm_to_huse`**: Add leads to Huse database
- **`POST /send_huse_credentials_email/<employee_id>`**: Send credentials email
- **`GET /employees/by_role/<role_name>`**: Get employees by role
- **`GET /users/by_username/<username>`**: Get employee by username

**Note**: The mood check workflow is typically invoked programmatically through the `employee_mood_check()` function, not directly via REST API.

---

## Setup & Configuration

### Prerequisites

- Python 3.7+
- PostgreSQL database
- Redis (for session management)
- OpenAI API key (for AI responses)

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/Employee

# API Keys
HUSE_API_KEY=your_huse_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_DEBUG=0
FLASK_ENV=production
```

### Installation Steps

1. **Clone/Download the module**
   ```bash
   cd "Employee Mood Module"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # If requirements.txt doesn't exist, install manually:
   pip install flask flask-sqlalchemy flask-migrate pydantic python-dotenv
   pip install openai redis sqlalchemy psycopg2-binary
   pip install numpy scipy  # For statistics
   ```

3. **Database Setup**
   ```bash
   # Initialize database migrations
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Run the application**
   ```bash
   python app.py
   # Or
   flask run
   ```

### Configuration Files

- **`database.py`**: Database connection configuration
- **`utils/ai_client.py`**: AI client setup (OpenAI)
- **`app.py`**: Flask app initialization

---

## Usage Examples

### Basic Mood Check Workflow

```python
from employee_mood_check import employee_mood_check

# First call - triggers follow-up question
employee_mood_check(
    contact_number="+971509784398",
    user_message="",  # Empty or initial message
    mood_record_id=53  # ID of the mood record created earlier
)

# Second call - employee provides feedback
employee_mood_check(
    contact_number="+971509784398",
    user_message="I'm feeling stressed due to workload",
    mood_record_id=53
)
```

### Getting Mood Statistics

```python
from proxies.employee_mood_proxy import EmployeeMoodProxy
from datetime import date

# Get statistics for a company
stats = EmployeeMoodProxy.get_mood_check_statistics(
    company_ids=[1, 2],
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)

print(stats['summary'])
print(stats['mood_distribution'])
print(stats['statistics'])
print(stats['risk_analysis'])
```

### Adding Comments to Mood Record

```python
from proxies.employee_mood_proxy import EmployeeMoodProxy

# Add comment to existing mood record
EmployeeMoodProxy.add_comment_to_mood_record_by_id(
    mood_id=53,
    comment="Employee mentioned workload concerns"
)
```

### Session Management

```python
from proxies.employee_mood_session_proxy import EmployeeMoodSessionProxy

# Check if feedback was asked
asked = EmployeeMoodSessionProxy.get_employee_asked_user_feedback("+971509784398")

# Set feedback flag
EmployeeMoodSessionProxy.set_employee_asked_user_feedback("+971509784398", True)

# Clear after completion
EmployeeMoodSessionProxy.clear_employee_asked_user_feedback("+971509784398")
```

---

## Dependencies

### Core Dependencies

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migrations
- **SQLAlchemy**: Database toolkit
- **psycopg2-binary**: PostgreSQL adapter

### AI & Utilities

- **openai**: OpenAI API client for AI responses
- **pydantic**: Data validation
- **python-dotenv**: Environment variable management

### Analytics

- **numpy**: Numerical computations for statistics
- **scipy**: Statistical functions

### Session Management

- **redis**: Session storage (if using Redis backend)

---

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify `DATABASE_URL` in `.env` file
   - Ensure PostgreSQL is running
   - Check database credentials

2. **AI Response Generation Fails**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check API quota/limits
   - Ensure model name is correct (`gpt-5.1` in code)

3. **Session Not Persisting**
   - Check Redis connection (if using Redis)
   - Verify session storage backend configuration
   - Check `SessionState` table in database

4. **Employee Not Found**
   - Verify employee exists in database
   - Check contact number format (should include country code)
   - Ensure employee record has valid `contactNo` field

5. **Mood Record Not Updating**
   - Verify `mood_record_id` is valid
   - Check database permissions
   - Review error logs for specific issues

### Debug Mode

Enable debug logging by setting:
```python
FLASK_DEBUG=1
```

The code includes extensive print statements for debugging:
- `[MoodCheck - Initialization]`
- `[MoodCheck - Employee Lookup]`
- `[MoodCheck - Feedback Check]`
- `[MoodCheck - Response Generation]`
- `[MoodCheck - Session Cleanup]`

---

## Key Concepts for Knowledge Transfer

### 1. **Mood Rating Scale**
- **1 = Great**: Employee is very satisfied
- **2 = Good**: Employee is satisfied
- **3 = Okay**: Employee is neutral/slightly dissatisfied
- **4 = Not so good**: Employee is dissatisfied

### 2. **Session Flow States**
- **Initial State**: No feedback requested
- **Feedback Requested**: Follow-up question sent, waiting for response
- **Feedback Received**: Response generated, session cleared

### 3. **Proxy Pattern**
- Proxies act as abstraction layer between business logic and services
- They handle Flask app context management
- Simplify database session handling

### 4. **Service Layer**
- Contains pure business logic
- No Flask dependencies
- Easily testable

### 5. **AI Integration**
- Uses OpenAI GPT models for response generation
- Structured output using Pydantic models
- Temperature settings control response creativity

### 6. **Statistics & Analytics**
- Comprehensive mood analysis
- Risk identification (employees with average mood ≥ 3.0)
- Trend analysis (improving/worsening/stable)
- Date-wise and employee-wise breakdowns

---

## Future Enhancements

Potential improvements for the module:

- [ ] REST API endpoint for mood check workflow
- [ ] Scheduled mood check reminders
- [ ] Email notifications for HR on negative ratings
- [ ] Dashboard for mood visualization
- [ ] Multi-language support
- [ ] Integration with HR management systems
- [ ] Automated escalation for critical feedback

---

## Support & Contact

For questions or issues:
1. Review the troubleshooting section
2. Check application logs
3. Verify database and API configurations
4. Contact the development team

---

**Last Updated**: 2024
**Version**: 1.0
**Maintained By**: Development Team


