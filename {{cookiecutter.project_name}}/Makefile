{% if cookiecutter.use_make == "y" %}
include .env


tail := 200

default:help

help:
	@echo "aiogram template"

{% if cookiecutter.use_isort == "y" and cookiecutter.use_black == "y" and cookiecutter.use_flake8 == "y" -%}
# ================================================================================================
# Linters and code formatters
# ================================================================================================

isort:
	poetry run isort .

black:
	poetry run black .

flake8:
	poetry run flake8 .

lint: isort black flake8
{% endif %}
# ================================================================================================
# Migrations
# ================================================================================================

alembic:
	poetry run alembic ${args}

migrate:
	poetry run alembic upgrade head

makemigrations:
	poetry run alembic revision --autogenerate -m "${message}"

downgrade:
	poetry run alembic downgrade -1

# ================================================================================================
# Docker
# ================================================================================================

docker-config:
	docker-compose config

docker-ps:
	docker-compose ps

docker-build:
	docker-compose build

docker-up-dependencies:
	docker-compose up -d redis db

docker-up:
	docker-compose up -d --remove-orphans

docker-stop:
	docker-compose stop

docker-down:
	docker-compose down

docker-destroy:
	docker-compose down -v --remove-orphans

docker-logs:
	docker-compose logs -f --tail=${tail} ${args}

# =================================================================================================
# Application in Docker
# =================================================================================================

app-create: docker-build app-start

app-logs:
	$(MAKE) docker-logs args="bot"

app-stop: docker-stop

app-down: docker-down

app-start: docker-stop docker-up

app-destroy: docker-destroy
{% endif %}