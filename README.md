# Acer School App API

A Django REST API for managing school-related data including grades, subjects, and KCSE (Kenya Certificate of Secondary Education) papers.

## Overview

This API provides endpoints for accessing and managing educational data, specifically designed for school management systems. It includes features such as:

- Grade management with letter grades, score ranges, and points
- Subject management with subject codes
- KCSE subject papers configuration with percentage weights

## Technology Stack

- **Backend**: Django 5.2.3 with Django REST Framework 3.16.0
- **Database**: PostgreSQL 15
- **Caching**: Redis 7
- **Containerization**: Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose
- Python 3.13.0 (for local development)

## Setup and Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/paulmbui20/acerschoolappapi.git
   cd AcerSchoolAppAPI
   ```

2. Create a `.env` file in the project root with the following variables:
   ```
   DJANGO_SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=db
   DB_PORT=5432
   
   REDIS_URL=redis://redis:6379/0
   REDIS_PASSWORD=
   
   PYTHON_VERSION=3.13.0
   UID=10001
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up
   ```

4. The API will be available at http://localhost:8005/

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/paulmbui20/acerschoolappapi.git
   cd AcerSchoolAppAPI
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the necessary environment variables
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Grades API

- **GET** `/sample/grades/`: Retrieve all grade information
  - Query Parameters:
    - `page_size`: Number of results per page
    - `page`: Page number
  - Response: List of grades with letter, score ranges, points, and comments

### Subjects API

- **GET** `/sample/subjects/`: Retrieve all subjects
  - Query Parameters:
    - `search`: Search by subject name or code
    - `page_size`: Number of results per page
    - `page`: Page number
  - Response: List of subjects with their codes and names

### KCSE Papers API

- **GET** `/sample/kcse-papers/`: Retrieve all KCSE subjects with their papers
  - Response: List of subjects with their associated papers, including paper names, maximum scores, and percentage weights

## Features

### Caching

The API implements Redis caching to improve performance. Responses are cached for 15 minutes with cache invalidation based on request parameters.

### Rate Limiting

API endpoints are protected with rate limiting:
- Anonymous users: 60 requests per hour
- Authenticated users: Default Django REST Framework rate limits

### Admin Interface

The Django admin interface is available for managing data with custom validation:
- Subject papers percentage weights must sum to 100%
- Grade ranges are properly ordered

## Project Structure

```
AcerSchoolAppAPI/
├── acerschoolappapi/       # Main project settings
├── sample/                 # Main application
│   ├── functions/          # Utility functions
│   ├── migrations/         # Database migrations
│   ├── views/              # API views
│   ├── admin.py            # Admin interface configuration
│   ├── models.py           # Database models
│   ├── serializers.py      # API serializers
│   └── urls.py             # URL routing
├── templates/              # HTML templates
├── .dockerignore           # Docker ignore file
├── .gitignore              # Git ignore file
├── build.sh                # Build script for Docker
├── compose.yaml            # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

