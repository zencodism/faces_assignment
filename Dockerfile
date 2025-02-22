# Use the official Python 3.8 slim image as the base image
FROM python:3.12-slim

RUN apt update && apt install -y gcc clang clang-tools cmake

# Set the working directory within the container
WORKDIR /faces

# Copy the necessary files and directories into the container
COPY app.py requirements.txt operations.py /faces/
COPY static/ /faces/static/
COPY templates/ /faces/templates/
RUN mkdir -p /faces/uploads

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# just to be sure
RUN pip3 install gevent

# Just a self-documenting note
EXPOSE 8282

# Gunicorn for flask, gevent needed for websockets
ENTRYPOINT ["gunicorn", "-k", "gevent", "-w", "1", "-b", ":8282", "app:app"]
