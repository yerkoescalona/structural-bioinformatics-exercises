.PHONY: lint help

help:
	@echo "lint   ruff check + format"

lint:
	uv run ruff check --fix .
	uv run ruff format .
