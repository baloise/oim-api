# This Dockerfile creates a compact development-only server

# Setting the base container
FROM quay.balgroupit.com/baloise-base-images/python:3.9.1-slim-buster

# Allows to specify build-time envvars for specific build networks
ADD ./.env.build* /tmp/

# Create a user and group to use within the container
RUN groupadd --gid 1000 apiserver
RUN useradd --uid 1000 --gid apiserver --no-log-init --no-create-home apiserver

# Copy all of the current (and sub) dir into the container during build
ADD . /code
# Define the starting working directory within the container
WORKDIR /code

# While building, install python dependencies
RUN \
  touch /tmp/.env.build && \
  export $(grep -v '^#' /tmp/.env.build | xargs -0) && \
  pip install -r requirements.txt && \
  rm -f /tmp/.env.build /code/.env.build

# Next we set defaults for some of the envvars
# NOTE: You MUST set more than these! See .env.sample file for a list.
ENV SERVER_PORT=9090

# Give a hint to docker where the service exposes
EXPOSE ${SERVER_PORT}

# Define the user to be used inside when running the container
USER apiserver:apiserver

# This defines the command that will run the actual starting process within the container
CMD ["python", "app.py"]
