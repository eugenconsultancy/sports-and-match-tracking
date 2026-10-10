#!/bin/bash

echo "========================================="
echo "  LiveScore Platform - Setup & Run"
echo "========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is required but not installed.${NC}"
    exit 1
fi

# Setup virtual environment
echo -e "${YELLOW}[1/8] Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}[2/8] Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Setup database
echo -e "${YELLOW}[3/8] Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

# Seed data
echo -e "${YELLOW}[4/8] Seeding sample data...${NC}"
python manage.py seed_data

# Create superuser (if not exists)
echo -e "${YELLOW}[5/8] Creating superuser...${NC}"
python manage.py createsuperuser --noinput || true

# Install frontend dependencies
echo -e "${YELLOW}[6/8] Installing frontend dependencies...${NC}"
cd frontend && npm install && cd ..

# Start services
echo -e "${YELLOW}[7/8] Starting backend services...${NC}"

# Start Django dev server
echo -e "${GREEN}Starting Django server on http://localhost:8000${NC}"
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Start Celery worker
echo -e "${GREEN}Starting Celery worker...${NC}"
celery -A core.celery_app worker -l info -Q default,live &
CELERY_PID=$!

# Start Celery beat
echo -e "${GREEN}Starting Celery beat...${NC}"
celery -A core.celery_app beat -l info &
CELERY_BEAT_PID=$!

# Start FastAPI real-time service
echo -e "${GREEN}Starting FastAPI real-time service on http://localhost:8001${NC}"
cd realtime && uvicorn main:app --host 0.0.0.0 --port 8001 --reload &
FASTAPI_PID=$!
cd ..

# Start frontend
echo -e "${YELLOW}[8/8] Starting frontend dev server...${NC}"
echo -e "${GREEN}Starting Vue frontend on http://localhost:5173${NC}"
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  All services are running!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "  Django API:      ${YELLOW}http://localhost:8000${NC}"
echo -e "  Django Admin:    ${YELLOW}http://localhost:8000/admin/${NC}"
echo -e "  API Docs:        ${YELLOW}http://localhost:8000/api/schema/swagger-ui/${NC}"
echo -e "  FastAPI WS:      ${YELLOW}http://localhost:8001${NC}"
echo -e "  Vue Frontend:    ${YELLOW}http://localhost:5173${NC}"
echo ""
echo -e "  Admin Credentials:"
echo -e "    Email:    ${YELLOW}admin@livescore.com${NC}"
echo -e "    Password: ${YELLOW}admin123${NC}"
echo ""
echo -e "${RED}Press Ctrl+C to stop all services${NC}"

# Trap Ctrl+C
trap "kill $DJANGO_PID $CELERY_PID $CELERY_BEAT_PID $FASTAPI_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

# Wait for any process to exit
wait