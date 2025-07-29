# Troubleshooting Guide

## Permission Denied Error on Windows

If you get the error: `exec: "/app/start.sh": permission denied`

### Solution 1: Use the Simple Docker Compose
```bash
docker-compose -f docker-compose.simple.yml up --build
```

### Solution 2: Fix Line Endings
The issue might be caused by Windows line endings (CRLF) instead of Unix line endings (LF).

1. Open `backend/start.sh` in a text editor that can change line endings (VS Code, Notepad++, etc.)
2. Change line endings to LF (Unix)
3. Save the file
4. Rebuild: `docker-compose up --build`

### Solution 3: Run Commands Directly
Instead of using docker-compose, run the containers manually:

```bash
# Backend
cd backend
docker build -t ledger-backend .
docker run -p 8000:8000 ledger-backend bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

# Frontend (in another terminal)
cd frontend
docker build -t ledger-frontend .
docker run -p 8080:8080 ledger-frontend
```

### Solution 4: Use Python Directly (No Shell Script)
Replace the Dockerfile with Dockerfile.alternative:

```bash
cd backend
copy Dockerfile.alternative Dockerfile
cd ..
docker-compose up --build
```

## Other Common Issues

### Ports Already in Use
```
Error: bind: address already in use
```

**Solution**: Change ports in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Module Not Found Errors
```
ModuleNotFoundError: No module named 'django'
```

**Solution**: Ensure requirements.txt is in the backend directory:
```bash
cd backend
copy ../requirements.txt .
```

### Frontend Build Errors
```
npm ERR! code ENOENT
```

**Solution**: Ensure package.json exists and is valid:
```bash
cd frontend
npm init -y
npm install vue@3 vue-router@4 axios
```

### Database Errors
```
django.db.utils.OperationalError
```

**Solution**: Delete the database and recreate:
```bash
docker-compose down -v
docker-compose up --build
```

## Running Without Docker

If Docker continues to cause issues, run the application directly:

### Backend (PowerShell/Command Prompt)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

### Frontend (Another Terminal)
```powershell
cd frontend
npm install
npm run serve
```