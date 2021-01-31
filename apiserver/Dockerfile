# This Dockerfile creates a compact development-only server

# Setting the base container
FROM python:3.8-alpine

# Create a user and group to use within the container
RUN groupadd -r apiserver && useradd --no-log-init -r -g apiserver apiserver
# Copy all of the current (and sub) dir into the container during build
ADD . /code
# Define the starting working directory within the container
WORKDIR /code
# While building, install python dependencies
RUN pip install -r requirements.txt

# Define the user to be used inside when running the container
USER apiserver:apiserver

# This defines the command that will run the actual starting process within the container
CMD ["python", "app.py"]
