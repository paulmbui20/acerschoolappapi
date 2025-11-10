# Acer School App API

A Django REST API for managing school-related data including grades, subjects, KCSE papers, and CBC (Competency Based Curriculum) learning areas and learning levels.

## Overview

This API provides endpoints for accessing structured educational data used in school management systems. It includes:

* Grade definitions with score ranges and points
* Subject definitions with official codes
* KCSE subject papers and weights
* CBC learning areas and learning levels
* High-performance caching with automatic invalidation
* Pagination, rate limiting, and optimized query handling

## Technology Stack

* **Backend**: Django 5.2.3
* **API Framework**: Django REST Framework 3.16.0
* **Database**: PostgreSQL 15
* **Caching**: Redis 7
* **Containerization**: Docker and Docker Compose

## Prerequisites

* Docker and Docker Compose
* Python 3.13.0 (optional for local/manual development)

---

# Setup and Installation

## Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/paulmbui20/acerschoolappapi.git
   cd AcerSchoolAppAPI
   ```

2. Create a `.env` file in the project root:

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

3. Start the stack:

   ```bash
   docker-compose up
   ```

4. The API will be available at:

   ```
   http://localhost:8005/
   ```

---

## Local Development (Without Docker)

1. Clone the repository
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Add a `.env` file at project root.
5. Run migrations:

   ```bash
   python manage.py migrate
   ```
6. Start development server:

   ```bash
   python manage.py runserver
   ```

---

# API Endpoints

This API is organized into modules. All examples assume the default local base URL:

```
http://localhost:8005/
```

---

# 1. Grades API (Sample App)

### **GET /sample/grades/**

Retrieve all grade definitions.

Query Parameters:

| Name      | Type | Description    |
| --------- | ---- | -------------- |
| page      | int  | Page number    |
| page_size | int  | Items per page |

Response returns a list of grade letters, score ranges, points, and comments.

---

# 2. Subjects API (Sample App)

### **GET /sample/subjects/**

Retrieve all subjects.

Query Parameters:

| Name      | Type   | Description                    |
| --------- | ------ | ------------------------------ |
| search    | string | Filter by subject code or name |
| page      | int    | Page number                    |
| page_size | int    | Items per page                 |

---

# 3. KCSE Papers API (Sample App)

### **GET /sample/kcse-papers/**

Retrieve all KCSE subjects and their configured papers.

Response includes paper names, maximum scores, and percentage weights.

---

# 4. CBC Learning Areas API (CBC App)

Base path:

```
/cbc/
```

## **GET /cbc/sample/learning-areas/**

Returns the full list of CBC learning areas.

Query Parameters:

| Name      | Type | Description    |
| --------- | ---- | -------------- |
| page      | int  | Page number    |
| page_size | int  | Items per page |

Response example:

```json
{
  "count": 9,
  "results": [
    { "id": 1, "name": "English", "code": "ENG" },
    { "id": 2, "name": "Mathematics", "code": "MATH" }
  ]
}
```

## **GET /cbc/sample/learning-areas/<id>/**

Retrieve a single learning area.

---

# 5. CBC Learning Levels API (CBC App)

## **GET /cbc/sample/learning-levels/**

Retrieve the full list of CBC learning levels (PP1, PP2, Grade 1–9).

Query parameters: `page`, `page_size`.

## **GET /cbc/sample/learning-levels/<id>/**

Retrieve a single learning level.

---

# Caching

The system uses **Redis caching with a 30-day TTL** and automatic invalidation:

* All list endpoints: cached by explicit list keys
* All detail endpoints: cached per object (`learningarea_detail_<id>`)
* On any update or delete:

  * Relevant detail cache is cleared
  * All list caches are cleared

Result: very fast reads, zero stale data.

---

# Rate Limiting

Rate limits (via DRF throttles):

* **Anonymous users**: 60 requests/hour
* **Authenticated users**: DRF defaults

---

# Admin Interface

The Django Admin panel supports:

* Managing grades
* Managing subjects
* Managing KCSE papers with validation (100% weight rule)
* Managing CBC learning areas and levels

---

# Project Structure

```
AcerSchoolAppAPI/
├── acerschoolappapi/       # Project settings
├── sample/                 # Grades, subjects, KCSE APIs
│   ├── views/
│   ├── models/
│   ├── serializers/
│   ├── migrations/
├── cbc/                    # CBC learning areas & levels APIs
│   ├── views/
│   ├── serializers/
│   ├── signals/
│   ├── migrations/
│   ├── urls.py
├── templates/
├── compose.yaml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---
