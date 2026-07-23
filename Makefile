.PHONY: install run test lint fmt docker-build docker-run clean

install:
	pip install -e .[dev]

run:
	python -m ai_agent.cli.main

test:
	pytest -v --cov=src/ai_agent tests/

lint:
	ruff check src/ tests/
	mypy src/
	bandit -r src/

fmt:
	ruff format src/ tests/

docker-build:
	docker build -t ai-agent .

docker-run:
	docker run --rm -it --env-file .env ai-agent

clean:
	rm -rf build/ dist/ *.egg-info htmlcov/ .pytest_cache/ .mypy_cache/ .coverage
