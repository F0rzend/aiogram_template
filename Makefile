include .env


tail := 200

default:help

help:
	@echo "aiogram template"

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

# ================================================================================================
# Migrations
# ================================================================================================

aerich:
	aerich ${args}

migrate:
	aerich upgrade

makemigrations:
	aerich migrate --name "${message}"

downgrade:
	aerich downgrade

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