# Text Ledger Application

A simple Django + Vue.js application for managing text ledger entries.

## Features

- User registration and authentication
- Add ledger entries (authenticated users only)
- View all ledger entries
- View detailed ledger entry
- View all users (authenticated users only)
- View user details (authenticated users only)

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or use the provided script
./run-docker.sh
```

The application will be available at:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000/api/

### Option 2: Manual Setup

#### Backend Setup (Django)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py makemigrations ledger
python manage.py migrate
```

6. Initialize test data (optional):
```bash
python init_data.py
```

7. Run the Django development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

#### Frontend Setup (Vue.js)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run serve
```

The frontend will be available at `http://localhost:8080`

### Option 3: Test Simulation

If you can't run the actual servers, use the test simulation:

```bash
python run-local-test.py
```

## Test Credentials

After running `init_data.py` or using Docker, you can login with:

- Email: `test@example.com`
  Password: `password123`

- Email: `demo@example.com`
  Password: `demo123`

## API Endpoints

- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login user
- `POST /api/logout/` - Logout user
- `GET /api/me/` - Get current user
- `GET /api/users/` - List all users (auth required)
- `GET /api/users/<id>/` - Get user details (auth required)
- `GET /api/ledger/` - List all ledger entries
- `POST /api/ledger/create/` - Create new ledger entry (auth required)
- `GET /api/ledger/<id>/` - Get ledger entry details
- `GET /api/health/` - Health check endpoint

## Project Structure

```
text-ledger-app/
├── backend/
│   ├── backend/          # Django project settings
│   ├── ledger/           # Main Django app
│   ├── manage.py         # Django management script
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Docker configuration
│   ├── start.sh          # Startup script
│   └── init_data.py      # Test data initialization
├── frontend/
│   ├── src/
│   │   ├── views/        # Vue components for pages
│   │   ├── router/       # Vue router configuration
│   │   ├── App.vue       # Main Vue component
│   │   └── main.js       # Vue entry point
│   ├── package.json      # Node dependencies
│   └── Dockerfile        # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── run-docker.sh         # Docker startup script
└── README.md            # This file
```

## Code Review Notes

This application was intentionally written with junior-level code patterns for educational purposes. It includes various inefficiencies and redundancies that could be improved. Some areas to review:

- Authentication implementation
- API design patterns
- Database query optimization
- Frontend state management
- Error handling
- Code duplication
- Security configurations

## Troubleshooting

1. **Port already in use**: Change the ports in `docker-compose.yml` or kill the processes using the ports
2. **Module not found**: Make sure all dependencies are installed with `pip install -r requirements.txt` and `npm install`
3. **CORS errors**: The backend is configured to allow all origins for development. This should be restricted in production
4. **Database errors**: Delete `db.sqlite3` and run migrations again