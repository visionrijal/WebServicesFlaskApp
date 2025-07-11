# Web Services API

A RESTful API for managing students, courses, and enrollments in a college system. Built with Flask, SQLAlchemy, and JWT authentication. Includes Docker support for easy deployment.

## Features
- JWT-based authentication (single admin user)
- CRUD for students, courses, enrollments
- SQLite database
- Modular project structure
- Dockerized for production

## Quick Start

### Docker
```bash
docker-compose up --build
```
API: http://localhost:5000
Docs: http://localhost:5000/docs/

### Manual
```bash
pip install -r requirements.txt
python run.py
```

## Authentication
- Username: `admin`
- Password: `webservices2024`

## API Endpoints
- `POST /auth/login` - Obtain JWT token
- `GET/POST/PUT/DELETE /students` - Manage students
- `GET/POST/PUT/DELETE /courses` - Manage courses
- `GET/POST/PUT/DELETE /enrollments` - Manage enrollments
- `GET /health` - Health check

## Project Structure
```
project/
  run.py
  models/
    __init__.py
    user.py
    student.py
    course.py
    enrollment.py
  routes/
    __init__.py
    auth.py
    students.py
    courses.py
    enrollments.py
  extensions.py
  config.py
  requirements.txt
  Dockerfile
  docker-compose.yml
```

## Docker Compose
```bash
docker-compose up --build
```

## License
MIT
