# Fixing Proxy Connection Error

The error `ECONNREFUSED` means the frontend cannot connect to the backend API.

## Quick Fixes

### 1. Make Sure Backend is Running

First, check if the backend is actually running:

```powershell
# In PowerShell, try to access the backend
curl http://localhost:8000/api/health/
```

If this fails, the backend isn't running.

### 2. Run Backend and Frontend Separately (Easiest)

**Terminal 1 - Start Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Terminal 2 - Start Frontend:**
```powershell
cd frontend
npm install
npm run serve
```

### 3. If Using Docker

The proxy configuration is already fixed for Docker. Make sure to:

1. Stop all containers:
```powershell
docker-compose down
```

2. Rebuild and start:
```powershell
docker-compose -f docker-compose.simple.yml up --build
```

3. Check that both containers are running:
```powershell
docker ps
```

You should see both `text-ledger-app-backend-1` and `text-ledger-app-frontend-1`.

### 4. Alternative: Direct API Calls

If proxy still doesn't work, modify the frontend to use direct API URLs:

Edit `frontend/src/main.js` and add:
```javascript
// Add this before createApp
import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000'
```

### 5. Windows Firewall

Sometimes Windows Firewall blocks the connection. Try:

1. Temporarily disable Windows Firewall
2. Or add an exception for ports 8000 and 8080

### 6. Use the Check Script

Run the provided script to diagnose:
```powershell
.\check-services.ps1
```

This will tell you exactly what's running and what's not.

## Common Scenarios

### Scenario A: Both Running Locally
- Backend: http://localhost:8000
- Frontend: http://localhost:8080
- Proxy should work automatically

### Scenario B: Using Docker
- Containers communicate via Docker network
- Use service names (backend, frontend) not localhost
- Already configured in docker-compose files

### Scenario C: Mixed (Not Recommended)
- If backend in Docker and frontend local (or vice versa)
- Need to use host machine's IP address
- More complex configuration required