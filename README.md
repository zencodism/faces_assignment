# Face detection assignment

This is a test assignment project showcasing a few different capabilities:

  - runs a simple Python webserver using Flask
  - gives it real-time comms channel with websockets (flask-socketio)
  - allows for photo upload with rudimentary sanity/security checks
  - hosts the photos uploaded, with updates pushed to connected clients
  - detects faces presented on photos, if any, and marks them before save
  - packages the above in a Docker image

## Setup

There is a Makefile provided as a self-documenting list of available actions.
In order to get the project up and running, `make setup` should suffice.
If it doesn't, or if in doubt,
  - create a virtualenv (typically `python -m virtualenv <venv_name>`),
  - activate it (`source <venv_name>/bin/activate`), and
  - install dependencies with `pip install -r requirements.txt`

The face detection library pulls dlib in turn, which introduces a requirement
to have cmake available on system.  

## Run

Local, debug server can be started with `python app.py`; additionally,
`make run` will start a more full featured Gunicorn webserver instance.

That said, the expected way of deploying the project is, as per requirements,
Docker image.

In any case the server will listen on http://0.0.0.0:8282

## Packaging

A pre-built image is available on the [release page](https://github.com/zencodism/faces_assignment/releases/tag/first_build).
It can be loaded into local docker setup via `docker load faces_assignment.tar`.

Alternatively, `make build-image` will create an image labeled 'faces_assignment'
based on included Dockerfile. The resulting image exposes port 8282, so upon 
running it, this one should be forwarded.

An example command opening an interactive console would be:

`docker run --rm -it -p 8282:8282 --name faces-container faces_assignment`

... or, `make launch`


## What this project isn't - or, limitations

This is a showcase, not a production ready application. A conscious decision was
made to stop at the point where the formal requirements are fulfilled to a point
reasonable to achieve in a few hours of work. Specifically:

  - there is no persistent database, ORM in use, etc
  - no memory of previously uploaded files - they are hosted based on filesystem
  path only
  - no real security, be it a https certificate, CORS, DDoS prevention, or any
  kind of user management
  - no test coverage - a single unit test is there just to show where to plug
  more if needed
  - no build system or pipeline definition
