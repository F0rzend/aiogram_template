.DEFAULT_GOAL := help

base_python := python3
py := poetry run
python := $(py) python

.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Start the bot"
	@echo "  install	Install dependencies"
	@echo "  update	Update dependencies"
	@echo "  flake		Run flake8"
	@echo "  black		Run black"
	@echo "  isort		Run isort"
	@echo "  lint		Reformat code"


# ================================================================================================
# Commands
# ================================================================================================

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	$(python) -m bot

.PHONY: update
update:
	poetry update

.PHONY:	black
black:
	$(python) -m black .

.PHONY: isort
isort:
	$(python) -m isort .

.PHONY: flake
flake:
	$(python) -m flake8 .

.PHONY: lint
lint: black isort flake
