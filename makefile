.PHONY: install test coverage publish

install:
	poetry install --no-dev --no-interaction

test:
	poetry run pytest -vv

coverage:
	poetry run pytest -vv --cov=symply tests/ --cov-report xml --cov-report term

publish:
	poetry publish --build
