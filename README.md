# FocusSprint - FastAPI Backend

<p align="center">

[![Docker CI](https://github.com/rahman-03/focussprint-fastapi/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/rahman-03/focussprint-fastapi/actions/workflows/docker-ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Pytest](https://img.shields.io/badge/Tests-27%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

</p>

## 🌐 Live Demo

| Service | Link |
|----------|------|
| 🚀 Frontend | https://focussprint.in |
| ⚡ Backend API | https://api.focussprint.in |
| 📖 Swagger UI | https://api.focussprint.in/docs |
| 📚 ReDoc | https://api.focussprint.in/redoc |
| 💻 Frontend Repository | https://github.com/rahman-03/focussprint-angular |

A scalable, containerized RESTful backend API for **FocusSprint**, a task management application. Built with **FastAPI**, **PostgreSQL**, **JWT Authentication**, and **Docker** for seamless local development and production deployment. The project features a comprehensive **Pytest**-based automated test suite to ensure reliability and maintainability. This API provides secure user authentication, complete task management functionality, and role-based admin user management.

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/rahman-03/focussprint-fastapi.git
cd focussprint_fastapi

# 2. Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (see example below)
# Copy environment variables from .env.example

# 5. Start server
uvicorn app.main:app --reload

# 6. Open browser
# http://127.0.0.1:8000/docs
```

> Tip: You can also run the backend with Docker instead of the local Python virtual environment. See the Docker section below.

---

## 🚀 Features

- JWT Authentication with Refresh Tokens
- User Registration & Login
- Secure Password Hashing
- CRUD Operations for Tasks
- User-specific Task Management
- Protected API Endpoints
- PostgreSQL Database
- SQLAlchemy ORM
- Input Validation with Pydantic
- CORS Support
- Error Handling
- Interactive API Documentation
- Admin User Management
- Comprehensive Automated API Testing with Pytest
- Dockerized Test Environment
- Isolated PostgreSQL Test Database
- Multi-stage Docker Build
- Multi-environment Docker Compose Configuration
- Dependency Injection & Mocking for Tests

---

## 🛠️ Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

### Authentication
- JWT
- Passlib (bcrypt)

### Testing
- Pytest
- FastAPI TestClient

### DevOps
- Docker
- Docker Compose
- GitHub Actions

### Deployment
- Render
- Neon PostgreSQL

---

## 🏗 Architecture

```
                           ┌─────────────────────┐
                           │        User         │
                           └──────────┬──────────┘
                                      │
                                  HTTPS
                                      │
                                      ▼
                  ┌──────────────────────────────────┐
                  │  Angular Frontend (Netlify)      │
                  └──────────┬───────────────────────┘
                             │
                      JWT Auth / REST API
                             │
                             ▼
                  ┌──────────────────────────────────┐
                  │   FastAPI Backend (Render)       │
                  │                                  │
                  │ • Authentication                 │
                  │ • Authorization (RBAC)           │
                  │ • Business Logic                 │
                  │ • REST API                       │
                  └──────────┬───────────────────────┘
                             │
                        SQLAlchemy ORM
                             │
                             ▼
                  ┌──────────────────────────────────┐
                  │ PostgreSQL Database (Neon)       │
                  └──────────────────────────────────┘
```

---

## 📂 Project Structure

```
focussprint_fastapi/
│
├── app/
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── hashing.py
│   │   ├── jwt.py
│   │   └── router.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   ├── todo.py
│   │   └── user.py
│   ├── routers/
│   │   ├── admin.py
│   │   ├── todos.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── todo.py
│   │   └── user.py
│   ├── database.py
│   └── main.py
|
├──test/
│   ├── __init__.py
│   ├── conftest.py
│   ├── utils.py
│   ├── test_main.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_todos.py
│   └── test_admin.py
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── docker-compose.test.yml
├── .dockerignore
│
├── pytest.ini
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

#### For Local Python Development:
- **Python 3.11** - [Download](https://www.python.org/downloads/)
- **PostgreSQL** - [Download](https://www.postgresql.org/download/)

#### For Docker:
- **Docker** - [Download](https://www.docker.com/products/docker-desktop)
- **Docker Compose** - Included with Docker Desktop

### Quick Start with Docker

The fastest way to get started is with Docker:

```powershell
# 1. Clone repository
git clone https://github.com/rahman-03/focussprint-fastapi.git
cd focussprint_fastapi

# 2. Create .env file (copy from .env.example)
# Copy environment variables from .env.example

# 3. Start the development stack with hot-reload
docker compose up --build

# 4. Open browser to API documentation
# http://127.0.0.1:8000/docs

# 5. Stop the stack when finished
docker compose down
```

### 1. Clone the Repository

```bash
git clone https://github.com/rahman-03/focussprint-fastapi.git
cd focussprint_fastapi
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

#### Windows (PowerShell)

```powershell
# Connect to PostgreSQL
psql -U postgres

# In psql terminal:
CREATE DATABASE focussprint;
\q
```

#### Linux / macOS

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# In psql terminal:
CREATE DATABASE focussprint;
\q
```

---

## 🔧 Environment Variables

Create a `.env` file in the project root. Copy from `.env.example` or use:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/focussprint"
TEST_DATABASE_URL="postgresql://username:password@localhost:5432/focussprint_test"

# JWT Configuration (min 32 characters)
ACCESS_SECRET_KEY="your_super_secret_access_key_with_min_32_chars_here"
REFRESH_SECRET_KEY="your_super_secret_refresh_key_with_min_32_chars_here"
ALGO="HS256"

# Frontend Configuration
FRONTEND_URL="http://localhost:4200"

**⚠️ Security Tips:**
- Never commit `.env` file to git
- Use strong, random secret keys
- Change defaults before production
- Store sensitive variables in secure vault

---

## ▶️ Run the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

Server will be available at: `http://127.0.0.1:8000`

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Custom Host/Port

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

---

## 🐳 Docker

The project uses multiple Docker Compose configurations for different environments.

| Compose File | Purpose |
|--------------|---------|
| `docker-compose.yml` | Base configuration shared across environments |
| `docker-compose.override.yml` | Local development with hot reload and bind mounts |
| `docker-compose.test.yml` | Automated testing with an isolated PostgreSQL container |
| `docker-compose.prod.yml` | Production deployment configuration |


### Local Development

This repository uses `docker-compose.yml` with `docker-compose.override.yml` for streamlined local development:

```powershell
docker compose up --build
```

The override file automatically provides:
- Project directory mounted into the container at `/app`
- Hot-reload enabled with `uvicorn --reload`
- Live code changes without container restart
- Port 8000 exposed for local testing

Stop the development stack:

```powershell
docker compose down
```

### Production Deployment

For production, do **not** use the dev override. Deploy using only the base compose file:

```powershell
# If override file is not present on server
docker compose -f docker-compose.yml up -d --build

# Or use a production override file (if available)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

**Optimization:** The repository includes a `.dockerignore` file to keep images small and builds fast by excluding unnecessary files (virtualenv, .git, __pycache__, etc.)

---

## 🐳 Docker Build Targets

| Target | Purpose |
|---------|---------|
| `development` | Local development with hot reload |
| `test` | Execute the Pytest suite |
| `production` | Optimized production image |

---

## �📖 API Documentation

**Swagger UI (Interactive):**
```
http://127.0.0.1:8000/docs
```

**ReDoc (Clean Documentation):**
```
http://127.0.0.1:8000/redoc
```

---

## 🧪 Testing

The project includes a comprehensive test suite built with **Pytest** and **FastAPI TestClient**.

### Test Coverage

- Authentication
- User Management
- Todo Management
- Admin Operations
- JWT Authentication
- Authorization
- Error Handling
- CRUD Operations

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -vv
```

### Run a Specific Test Module

```bash
pytest test/test_todos.py
```

### Run a Specific Test

```bash
pytest test/test_todos.py::test_create_todo
```
### Run Tests in Docker

```bash
docker compose \
  --env-file .env.test \
  -f docker-compose.yml \
  -f docker-compose.test.yml \
  up --build --abort-on-container-exit
```

This command builds the test image, starts an isolated PostgreSQL container, executes the complete Pytest suite, and automatically shuts down the test environment after completion.

> **Note**
>
> `.env.test` is used only for local Docker-based testing and is intentionally excluded from version control.
>
> GitHub Actions injects the required environment variables through repository secrets and workflow environment variables, so `.env.test` is **not** required in CI.

### The automated testing infrastructure includes:

- 27+ Pytest test cases
- Dockerized PostgreSQL test database
- FastAPI dependency overrides
- Pytest fixtures
- FastAPI TestClient
- Automatic database cleanup
- Authentication & Authorization testing
- CRUD endpoint testing
- Admin endpoint testing

---

## 🔄 Continuous Integration

Every push and pull request automatically:

- Builds the Docker image
- Starts an isolated PostgreSQL test database
- Executes the complete Pytest suite
- Reports test results through GitHub Actions

The project uses Docker-based CI to ensure the application behaves consistently across local development and automated pipelines.

---

## 🚀 Continuous Deployment

The production backend is automatically deployed to **Render** whenever changes are merged into the `main` branch.

Current deployment workflow:

```text
Feature Branch
      │
      ▼
Pull Request
      │
      ▼
GitHub Actions (Docker CI)
      │
      ▼
Merge to main
      │
      ▼
Render Automatic Deployment
      │
      ▼
Live API
```

---

## 🔐 Authentication

This project uses **JWT Bearer Tokens** with Access & Refresh tokens.

### Login Flow

1. POST `/auth/login` with credentials
2. Receive `access_token` and `refresh_token` (in httponly cookie)
3. Include in request header:
   ```
   Authorization: Bearer <access_token>
   ```

### Refresh Token

When access token expires:
```bash
POST /auth/refresh
# Returns new access token
```

---

## 📌 Main API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login with credentials |
| POST | `/auth/refresh` | Refresh access token via refresh cookie |

### User Management

| Method | Endpoint | Description |
|---------|----------|----------|
| POST | `/user/create_user` | Create new user |
| GET | `/user` | Get current user profile |
| PUT | `/user/change_pass` | Change user password |
| PUT | `/user/details_change` | Update user details |
| GET | `/admin/users` | Get all users (admin only) |
| GET | `/admin/user/{user_id}` | Get user by ID (admin only) |
| PUT | `/admin/user_update/{user_id}` | Update user (admin only) |
| DELETE | `/admin/user/{user_id}` | Delete user (admin only) |

### Tasks Management

| Method | Endpoint | Description |
|---------|----------|----------|
| GET | `/todos` | Get all user tasks |
| GET | `/todos/{todo_id}` | Get task by ID |
| POST | `/todos` | Create new task |
| PUT | `/todos/{todo_id}` | Update task |
| DELETE | `/todos/{todo_id}` | Delete task |
| DELETE | `/todos/deleteall` | Delete all user tasks |

---

## 🚨 Troubleshooting

### Port 8000 Already in Use

**Windows (PowerShell):**
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill process by PID
Stop-Process -Id <PID> -Force

# Alternative: Use different port
uvicorn app.main:app --port 3000 --reload
```

**Linux / macOS:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Alternative: Use different port
uvicorn app.main:app --port 3000 --reload
```

### Database Connection Failed

```
Error: could not connect to server
```

**Solutions:**
1. Ensure PostgreSQL is running
   ```bash
   # Windows: Check Services (services.msc)
   # Linux: sudo systemctl status postgresql
   # macOS: brew services list
   ```

2. Verify DATABASE_URL in `.env` file
   ```bash
   # Test connection
   psql -U username -d focussprint -h localhost
   ```

3. Check username/password credentials

4. Create database if missing:
   ```bash
   psql -U postgres -c "CREATE DATABASE focussprint;"
   ```

### Invalid Secret Key Error

**Error:** `Secret key must be at least 32 characters`

**Solution:**
- Generate strong secret keys:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Paste into `.env` file
- Both `ACCESS_SECRET_KEY` and `REFRESH_SECRET_KEY` must be 32+ chars

### Module Not Found: `app`

**Solution:**
```bash
# Ensure you're in project root directory
cd focussprint_fastapi

# Reinstall dependencies
pip install -r requirements.txt

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;.        # Windows
```

### CORS Error in Frontend

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Update `.env` with correct frontend URL:
  ```env
  FRONTEND_URL="http://localhost:4200"
  ```
- Restart backend server

---

## ✅ Security Features

- 🔒 Password Hashing (bcrypt)
- 🎫 JWT Authentication with expiration
- 🔄 Refresh Token rotation
- 🛡️ Protected Routes (role-based access)
- ✔️ Input Validation (Pydantic)
- 👤 User-specific Data Access
- 🔐 Secure Environment Variables
- 🚫 CORS Protection
- 📝 SQL Injection Prevention (SQLAlchemy ORM)
- ✅ Automated API Testing

---

## 🎯 Roadmap & Project Progress

### ✅ Completed (v1.0)

- [x] User Registration & Login
- [x] JWT Authentication with Refresh Tokens
- [x] Role-Based Access Control (Admin/User)
- [x] Secure Password Hashing (bcrypt)
- [x] Todo CRUD Operations
- [x] User Profile Management
- [x] Admin User Management
- [x] PostgreSQL Database Integration
- [x] SQLAlchemy ORM
- [x] Input Validation with Pydantic
- [x] Comprehensive Error Handling
- [x] Interactive API Documentation (Swagger UI & ReDoc)
- [x] Dockerized Development Environment
- [x] Multi-stage Docker Build
- [x] Docker Compose (Development, Testing & Production)
- [x] Automated Testing with Pytest
- [x] Dockerized PostgreSQL Test Environment
- [x] GitHub Actions Continuous Integration
- [x] Automated Deployment to Render on Push to Main

---

### 🚀 Short Term (v1.1)

- [ ] Email Verification
- [ ] Password Reset
- [ ] Task Categories & Tags
- [ ] Due Dates & Reminders
- [ ] Pagination & Filtering
- [ ] Rate Limiting

---

### 🚀 Medium Term (v1.2)

- [ ] Task Priorities
- [ ] Subtasks
- [ ] Task Status Workflow
- [ ] Task Sharing
- [ ] Task Comments
- [ ] File Attachments

---

### 🌟 Long Term (v2.0)

- [ ] Real-time Notifications (WebSockets)
- [ ] Two-Factor Authentication (2FA)
- [ ] User Profiles & Avatars
- [ ] Task Templates
- [ ] Activity Logs
- [ ] Productivity Dashboard
- [ ] Time Tracking
- [ ] Recurring Tasks
- [ ] Calendar View
- [ ] Slack & Google Calendar Integration
- [ ] Publish Docker Images to GitHub Container Registry (GHCR)
- [ ] Deploy Production from GitHub Container Registry

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Branch Naming
```
feature/task-categories
bugfix/login-error
docs/api-endpoints
```

### Commit Messages
```
feat: add task categories
fix: resolve login authentication issue
docs: update API documentation
refactor: improve database queries
```

### Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open Pull Request with description

---

## 🌐 Related Projects

| Project | Link |
|----------|------|
| Frontend Repository | https://github.com/rahman-03/focussprint-angular |
| Backend Repository | https://github.com/rahman-03/focussprint-fastapi |
| Live Frontend | https://focussprint.in |
| Live Backend | https://api.focussprint.in |

---

## 📄 License

This project is licensed under the **MIT License** - see LICENSE file for details.

---

## 👨‍💻 Author

**Abdul Rahman M**

- GitHub: https://github.com/rahman-03
- LinkedIn: https://www.linkedin.com/in/abdul-rahman-m-660158206

---

## 📞 Support

For issues, questions, or suggestions:
- Open GitHub Issue: https://github.com/rahman-03/focussprint-fastapi/issues
- Email: indmabdulrahman@gmail.com

**Happy coding! 🚀**