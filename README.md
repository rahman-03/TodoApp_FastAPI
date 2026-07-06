# FocusSprint - FastAPI Backend

A scalable RESTful backend API for **FocusSprint**, a task management application built with **FastAPI**, **PostgreSQL**, and **JWT Authentication**. This API provides secure user authentication and complete task management functionality.

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

---

## 🛠️ Tech Stack

- Python 3.x
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT (JSON Web Tokens)
- Passlib (Password Hashing)
- Uvicorn
- python-dotenv

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
│
├── requirements.txt
├── .env.example
├── .env
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL** - [Download](https://www.postgresql.org/download/)

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

# Optional: Server Configuration
SERVER_HOST="127.0.0.1"
SERVER_PORT="8000"
```

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

## 📖 API Documentation

**Swagger UI (Interactive):**
```
http://127.0.0.1:8000/docs
```

**ReDoc (Clean Documentation):**
```
http://127.0.0.1:8000/redoc
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
| GET | `/users/` | Get current user profile |
| PUT | `/users/` | Update user profile |
| GET | `/admin/users` | Get all users (admin only) |
| PUT | `/admin/users/{user_id}` | Update user (admin only) |
| DELETE | `/admin/users/{user_id}` | Delete user (admin only) |

### Tasks Management

| Method | Endpoint | Description |
|---------|----------|----------|
| GET | `/todos/` | Get all user tasks |
| GET | `/todos/todo/{id}` | Get task by ID |
| POST | `/todos/todo` | Create new task |
| PUT | `/todos/todo/{id}` | Update task |
| DELETE | `/todos/todo/{id}` | Delete task |

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

---

## 🎯 Roadmap & Future Enhancements

### Short Term (v1.1)
- [ ] Email verification on signup
- [ ] Password reset functionality
- [ ] Task categories and tags
- [ ] Due dates and reminders

### Medium Term (v1.2)
- [ ] Task priorities (High/Medium/Low)
- [ ] Subtasks support
- [ ] Task status tracking (Todo/In Progress/Done/Blocked)
- [ ] Task sharing with other users
- [ ] Task comments and discussions

### Long Term (v2.0)
- [ ] Real-time notifications
- [ ] Two-Factor Authentication (2FA)
- [ ] User profiles with avatars
- [ ] Task templates
- [ ] Activity logs
- [ ] Analytics & productivity dashboard
- [ ] Time tracking on tasks
- [ ] Recurring tasks
- [ ] Calendar view
- [ ] API integrations (Slack, Google Calendar)
- [ ] Docker containerization
- [ ] CI/CD Pipeline

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

**Angular Frontend:**
- Repository: https://github.com/rahman-03/focussprint-angular
- Live: https://focussprint.in

**Deployed Backend:**
- API: https://focussprint.onrender.com

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