.PHONY: help install migrate seed superuser run-backend run-celery run-fastapi run-frontend run-all docker-up docker-down clean

help:
	@echo "LiveScore Platform Commands"
	@echo "=========================="
	@echo "make install       - Install all dependencies"
	@echo "make migrate       - Run database migrations"
	@echo "make seed          - Seed sample data"
	@echo "make superuser     - Create superuser"
	@echo "make run-backend   - Run Django server"
	@echo "make run-celery    - Run Celery worker"
	@echo "make run-fastapi   - Run FastAPI real-time service"
	@echo "make run-frontend  - Run Vue frontend"
	@echo "make run-all       - Run all services"
	@echo "make docker-up     - Start Docker containers"
	@echo "make docker-down   - Stop Docker containers"

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

migrate:
	python manage.py makemigrations
	python manage.py migrate

seed:
	python manage.py seed_data

superuser:
	python manage.py createsuperuser

run-backend:
	python manage.py runserver 0.0.0.0:8000

run-celery:
	celery -A core.celery_app worker -l info -Q default,live

run-celery-beat:
	celery -A core.celery_app beat -l info

run-fastapi:
	cd realtime && uvicorn main:app --host 0.0.0.0 --port 8001 --reload

run-frontend:
	cd frontend && npm run dev

run-all:
	@echo "Starting all services..."
	@echo "Run each in a separate terminal:"
	@echo "  make run-backend"
	@echo "  make run-celery"
	@echo "  make run-celery-beat"
	@echo "  make run-fastapi"
	@echo "  make run-frontend"

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf venv frontend/node_modules frontend/dist