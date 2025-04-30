# 🌍 Disaster Alert System

A Django-based web application that provides real-time alerts for natural disasters using map visualization, user preferences, and global/regional filtering.

## Features

- User registration and authentication
- Personalized disaster alert preferences (by region and disaster type)
- Interactive map using Leaflet.js with marker clustering
- Filter alerts: Global / India / User-specific
- Alert source links for detailed information

## Tech Stack

- **Backend**: Django, PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js, Select2
- **Environment**: Python 3.x, Virtualenv
- **APIs**: Integrated with external disaster alert APIs (e.g. GDACS)

## Setup

1. Clone the repository  
   `git clone https://github.com/your-username/disaster-alert.git`

2. Create virtual environment  
   `python -m venv env && source env/bin/activate` (Linux/macOS)  
   `env\Scripts\activate` (Windows)

3. Install dependencies  
   `pip install -r requirements.txt`

4. Configure `.env` and database credentials in `settings.py`

5. Apply migrations  
   `python manage.py migrate`

6. Run the server  
   `python manage.py runserver`

## Modules

- `alerts/` – Main app for alert handling and preferences
- `disaster_alert/` – Project configuration and routing
- `templates/` – HTML templates
  

## Notes

- PostgreSQL is used in production; `.env` handles sensitive DB credentials.
- Virtual environment and `.env` are excluded using `.gitignore`.
