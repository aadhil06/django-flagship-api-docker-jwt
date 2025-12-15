# 🚀 Flagship Django REST API — Task Manager
This project serves as a production-ready backend blueprint for a secure, containerized Task Management API, demonstrating industry best practices.

## 🛠 Tech Stack

- **Backend:** Python 3.11, Django 5.x, Django REST Framework (DRF)
- **Database:** PostgreSQL (Containerized)
- **Authentication:** JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
- **Containerization:** Docker & Docker Compose

## ✨ Key Features

- **Containerized Environment :**
Fully isolated setup using Docker Compose (web, db).

- **Secure Authentication :**
Token-based access control using JWT.

- **Efficiency :**
Global application of LimitOffsetPagination on all list views.

- **Non-Trivial Business Rule :**
Enforces a logic gate preventing any user from creating more than 3 active Critical (Priority 5) tasks.

- **Reliability :**
Comprehensive unit tests covering authentication, CRUD operations, and business rule validation.


## ⚙️ Quick Start (Run Locally)

### Prerequisites

- **Docker**

- **Docker Compose**

**Setup Environment**

- Ensure the project structure is complete and the `.env` file is populated with database credentials.

**Build and Run Services**

```bash
docker-compose up --build -d
```

**Create Superuser (For API Access)**
```bash
docker-compose exec web python manage.py createsuperuser
```


## 🔗 Sample API Endpoints
```bash
| Purpose           | Method   | Endpoint      | Requires Token?  |
|-------------------|----------|---------------|------------------|
| Login             | POST     | `/api/token/` | No               |
| List/Create Tasks | GET/POST | `/api/tasks/` | Yes              |
```
