.PHONY: help setup install run test lint clean

help:
	@echo "Available commands:"
	@echo "  setup         Create a virtual environment and install dependencies using pipenv."
	@echo "  install       Install project dependencies using pipenv."
	@echo "  run           Start the FastAPI server."
	@echo "  test          Run tests."
	@echo "  lint          Run linting checks."
	@echo "  clean         Remove the virtual environment and any generated files."

setup:
	pipenv install -r tests/requirements.txt --dev

install:
	pipenv install -r requirements.txt

run:
	pipenv run uvicorn myserver.main:app --reload --port 8080

test: setup
	pipenv run pytest

lint:
	pipenv run flake8

clean:
	pipenv --rm

format:
	pipenv run yapf -i -r .
