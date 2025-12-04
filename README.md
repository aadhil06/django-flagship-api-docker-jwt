# 🚀 Flagship Django REST API: Task Manager

This project serves as a production-ready backend blueprint for a secure, containerized Task Management API, demonstrating industry best practices.

## 🛠 Tech Stack

  **Backend:** Python 3.11, Django 5.x, Django REST Framework (DRF)

  **Database:** PostgreSQL (Containerized)

  **Authentication:** JWT (JSON Web Tokens) via djangorestframework-simplejwt

  **Containerization:** Docker & Docker Compose


## ✨ Key Features

**1. Containerized Environment:** Fully isolated setup using Docker Compose (services: web and db).

**2. Secure Authentication:** Token-based access control (JWT).

**3. Efficiency:** Global application of LimitOffset Pagination on all list views.

**4. Non-Trivial Business Rule:** Enforcement of a logic that prevents any single user from creating more than 3 active Critical Priority (Priority 5) tasks.

**5. Reliability:** Comprehensive Unit Tests covering authentication, CRUD, and the core business rule.

## ⚙️ Quick Start (Run Locally)

**Prerequisites:** Install Docker and Docker Compose.

Setup Environment: Ensure the project structure is complete and the .env file is populated with database credentials.

### Build and Run Services:

    docker-compose up --build -d

(The -d runs the services in the background)

### Create Superuser (for API Access):

    docker-compose exec web python manage.py createsuperuser

| Purpose             | Method | Endpoint                                                   | Requires Token? |
| ------------------  | ------ | -----------------------------------------------------------| --------------- |
|  Login / Obtain JWT | POST   | `/api/token/`                                              | No              |
|  List/Create Tasks  | GET/   | `/api/tasks/`                                              | Yes             |
|                     |  POST  |                                                            |                 |
|  Run Tests          |  EXEC  |  `docker-compose exec web python manage.py test `          |   N/A           |






