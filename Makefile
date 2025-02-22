ifeq ($(shell command -v podman 2> /dev/null),)
    CMD=docker
else
    CMD=podman
endif

setup:
	python3 -m virtualenv venv
	venv/bin/pip install -r requirements.txt
	mkdir -p uploads

lint:
	ruff check .
	ruff format .
	isort .

test:
	PYTHONPATH=. ./venv/bin/pytest ./tests

run:
	gunicorn -k gevent -w 1 -b :8282 app:app

build-image:
	$(CMD) build -t faces_assignment .

launch:
	$(CMD) run --rm -it -p 8282:8282 --name faces-container faces_assignment
