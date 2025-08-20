.PHONY: up build logs shell makemig mig test lint fmt audit

up:
	docker compose up -d

build:
	docker compose build

logs:
	docker compose logs -f web

shell:
	docker compose exec web bash

makemig:
	docker compose exec web python manage.py makemigrations

mig:
	docker compose exec web python manage.py migrate

test:
	docker compose exec web pytest -q

lint:
	docker compose exec web ruff check .
	docker compose exec web isort --check-only .
	docker compose exec web black --check .

fmt:
	docker compose exec web isort .
	docker compose exec web black .

audit:
	docker compose exec web pip-audit
