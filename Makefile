lint:
	ruff check .
	ruff format .
	isort .

setup:
	python3 -m virtualenv venv
	venv/bin/pip install -r requirements.txt
	mkdir -p uploads
