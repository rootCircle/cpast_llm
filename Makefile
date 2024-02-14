init:
	poetry install # make sure poetry is installed
	poetry run maturin develop

lint:
	poetry run ruff check .
	poetry run pyright # static type checking

run:
	poetry run maturin develop
	poetry run python3 main.py

fmt:
	poetry run ruff format

test:
	poetry run pytest

precommit: lint fmt test
