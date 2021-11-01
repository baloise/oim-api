# This Dockerfile creates a compact development-only server

# Setting the base container
FROM python:3.8-alpine

ADD ./.env.build* /tmp/

RUN \
  touch /tmp/.env.build && \
  export $(grep -v '^#' /tmp/.env.build | xargs -0) && \
  apk update && \
  apk add g++ gcc libxml2 libxslt libxslt-dev

# Create a user and group to use within the container
RUN addgroup -S apiserver && adduser -S apiserver -G apiserver

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
