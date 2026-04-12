# News Sentiment Analysis Dashboard

A Django web application that aggregates and analyzes sentiment from news articles across different sources. The application features a real-time dashboard displaying sentiment trends and article details with filtering capabilities.

## Features

- Real-time sentiment analysis of news articles (fetches data every hour)
- Interactive dashboard with Chart.js visualization displaying daily sentiment trends
- Filter articles by source and sentiment
- Paginated article listing with clickable headlines linking to original sources
- Automated and robust news fetching using Celery
- Multi-source news aggregation
- Sentiment classification (Positive, Neutral, Negative)

## Technology Stack

- Python 3.12+
- Django 5.2+
- MySQL Database
- VADER (for sentiment analysis)
- Redis (for Celery message broker)
- Celery (for background tasks)
- Chart.js (for data visualization)
- Bootstrap 5 (for UI components)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- MySQL Server
- Redis (Linux/Mac) or Memurai (Windows)
- Git

### Installing Redis/Memurai

#### For Windows Users (Memurai)

1. Download Memurai from the official website:
   ```
   https://www.memurai.com/get-memurai
   ```

2. Run the installer and follow the installation wizard
3. Memurai will start automatically and run as a Windows service
4. Verify installation by opening PowerShell and running:
   ```powershell
   memurai-cli ping
   ```
   You should receive a "PONG" response

#### For Linux/Mac Users (Redis)

1. **Ubuntu/Debian**:
   ```bash
   sudo apt update
   sudo apt install redis-server
   ```

2. **Mac (using Homebrew)**:
   ```bash
   brew install redis
   ```

3. Start Redis service:
   - Ubuntu/Debian: `sudo systemctl start redis`
   - Mac: `brew services start redis`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/brandonkongwe/news-sentiment.git
   cd news-sentiment
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   SECRET_KEY=your_secret_key
   DB_NAME=your_database_name
   USER=your_database_user
   PASSWORD=your_database_password
   HOST=localhost
   PORT=3306
   NEWS_API_KEY=your_newsapi.org_api_key
   ```

5. Set up the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. Start Redis/Memurai if not running as a service:
   ```bash
   # Windows (Memurai should be running as a service)
   # Linux/Mac
   redis-server
   ```

2. Start Celery worker (in a separate terminal):
   ```bash
   # Windows
   celery -A config worker -l INFO -P solo
   # Linux/Mac
   celery -A config worker -l INFO
   ```

3. Start Celery beat for scheduled tasks (in a separate terminal):
   ```bash
   celery -A config beat -l INFO
   ```

4. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application:
   - Dashboard: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

```
news-sentiment/
├── config/                 # Project configuration
│   ├── __init__.py
│   ├── celery.py          # Celery configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── news/                  # Main application
│   ├── migrations/
│   ├── templates/
│   │   └── news/
│   │       └── dashboard.html
│   ├── __init__.py
│   ├── admin.py          # Admin interface configuration
│   ├── apps.py
│   ├── models.py         # Database models
│   ├── services.py       # Business logic services
│   ├── tasks.py          # Celery tasks
│   ├── urls.py           # App URL configuration
│   └── views.py          # View controllers
├── .env                  # Environment variables
├── .gitignore
├── manage.py
└── requirements.txt
```

## Configuration

### Celery Task Schedule

The application is configured to fetch news every hour (the first scheduled fetch will only happen at the next hour mark. For example, if you start at 10:15, it will run at 11:00). To modify the schedule:

1. Access the Django admin interface
2. Navigate to "Periodic Tasks"
3. Modify the "fetch-news-every-hour" task


## Troubleshooting

### Common Issues

1. **Celery won't start**
   - Verify Redis/Memurai is running
   - Check Redis connection settings
   - Ensure virtual environment is activated

2. **Database connection errors**
   - Verify MySQL is running
   - Check database credentials in .env
   - Ensure database exists

3. **Missing articles**
   - Check Celery logs for task execution
   - Verify source URLs are accessible
   - Check API rate limits

## Acknowledgments

- [NewsAPI](https://newsapi.org)