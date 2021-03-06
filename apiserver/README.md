# apiserver

![apiserverCI](https://github.com/baloise/oim-api/workflows/apiserverCI/badge.svg)

- [apiserver](#apiserver)
  - [Development environment](#development-environment)
    - [Tools recommended for a local development environment](#tools-recommended-for-a-local-development-environment)
  - [Instructions for use](#instructions-for-use)
    - [Scenario: Local installation (no containers)](#scenario-local-installation-no-containers)
    - [Scenario: Containers (docker-compose)](#scenario-containers-docker-compose)
    - [Scenario: Kubernetes](#scenario-kubernetes)
  - [Additional notes](#additional-notes)
  - [Testing](#testing)
  - [Examples](#examples)
    - [DB Order Request Body](#db-order-request-body)
    - [JBoss Order Request Body](#jboss-order-request-body)
    - [Linux Order Request Body](#linux-order-request-body)
    - [Windows Order Request Body](#windows-order-request-body)

## Development environment

This chapter describes the development environment setup and gives random tips. 
This is intended to give an easier start but is in no way a complete and detailed step-by-step instruction set. Mostly the tools are listed and only few commands are given. __It is expected that can install AND configure them on your own.__

### Tools recommended for a local development environment
* A local [python](https://python.org) installation. Python 3.8 or newer recommended but 3.6+ is required currently.
  * To work inside the `apiserver` folder, create a local virtualenv: `python3 -m venv venv`
  * Activate the venv: *Depends on OS and shell*, for Bash and zsh: `. ./venv/bin/activate`
  * Verify that the venv has been activated: either `which python` spitting out a path inside your repo or check the command line for indications like a "(venv)" tag.
  * Install the dependencies into it (might require correct proxy settings):
    * `pip install -r requirements.txt`
    * If you intend to run the production-grade server, also do `pip install -r requirements.uwsgi.txt` (This may need a C compiler!)

* On Windows, Python does not look at the system certificate, it uses its own located at [venv]\lib\site-packages\certifi\cacert.pem. One of the following should
  solve issues with self-signed certificates (e.g. used by ourCloud):
  * `pip install python-certifi-win32`
  * download the certificate as pem/crt file (e.g. using browser) and append to cacert.pem.

* A Git client of your choice
  * Any git client that you prefer goes.
  * If you don't know any, check [this list](https://git-scm.com/downloads/guis/) or ask your colleagues

* [Visual Studio Code](https://code.visualstudio.com) (or another IDE of your choice)
  * Recommended vscode extensions:
    * [Python](vscode:extension/ms-python.python)
    * [Markdown All in One](vscode:extension/yzhang.markdown-all-in-one)
    * [YAML](vscode:extension/redhat.vscode-yaml)
    * [OpenAPI (Swagger) Editor](vscode:extension/42Crunch.vscode-openapi)
    * [openapi-lint](vscode:extension/mermade.openapi-lint)
    * [gitignore](vscode:extension/codezombiech.gitignore)
    * [DotENV](vscode:extension/mikestead.dotenv)
    * [Python Test Explorer for Visual Studio Code](vscode:extension/LittleFoxTeam.vscode-python-test-adapter)
    * [Docker](vscode:extension/ms-azuretools.vscode-docker) (if you have docker running locally)
    * [GitLens](vscode:extension/eamodio.gitlens) (optional)
    * [Rewrap](vscode:extension/stkb.rewrap) (optional)
    * _For VSCode on Windows/DWP only_: [Remote - SSH](vscode:extension/ms-vscode-remote.remote-ssh)

* Optional: [Docker](https://www.docker.com/get-started)
  
* Optional: docker-compose
  * Can be installed with `pip install docker-compose` if you followed the steps above and have a running local python.


## Instructions for use

To run the development or production versions of this api server see the following sub-chapters.

### Scenario: Local installation (no containers)

* Create local configuration:
  * `cp .env.sample .env`
  * Edit `.env` and fill the variables in there with correct values.
  * Current are the following:
  
    ```json
    OC_AUTH_USER=changeme             # currently not used
    OC_AUTH_PASS=changeme             # currently not used
    # OIM specific parameters
    BASEURL="https://localhost:9090/oimapi"
    SERVER_NAME="http://localhost"
    SERVER_PORT="9090"
    SPECDIR="openapi/"
    LOGGING_CONFIGFILE="logging.conf"
    LOGGING_LOGFILE="oim_error.log"
    LOGGING_MAILHOST=""
    DEBUG=False
    ```
  * You may need to ask your collegues for the correct values.

* Run the development server:
  * Verify you're still in the venv (see above)
  * Run the local development server: `python app.py`
  * See output to find the URL to connect to the development server. By default this is: http://0.0.0.0:9090/

* The development server has limited auto-reload functionality that reloads the server on code changes. However this does NOT seem to work on openapi/ yaml files and other code at the moment. It is recommended to restart the server manually on code changes. 

* To increase debugging even more: set this envvar: **FLASK_ENV=development**  But keep in mind that this may break some API output as it can result in human-friendly colorful HTML exception display rather than expected JSON returns.

* To stop the development server, hit CTRL+C


### Scenario: Containers (docker-compose)

This scenario is not yet fully documented. There are only some general notes for now:

* Make sure you have docker installed and the permissions to use it: `docker info`
* Make sure you have a recent version of docker-compose installed (see Tools chapter above)
* In the top level of this repo __(not in the apiserver folder!)__ there is an initial `docker-compose.dev.yaml` file prepared.
* This also expects the `.env` file to be __in the apiserver folder__ and contain your local configuration! (See Local installation chapter above)
* Switch to the top level directory of the repo.
* `docker-compose -f docker-compose.dev.yaml up` to bring the development server up
* `docker-compose -f docker-compose.dev.yaml up` to bring the development server down
* To force docker-compose to rebuild the image (like when you changed your code) you can add a `--build` behind the up-call.
* At a later stage this repo will contain the necessary docker-compose code to also pull up and link an nginx as a front webserver

### Scenario: Kubernetes

*No instructions available at this time.*


## Additional notes
* The server currently has no index handler. Don't freak out when you get an error message on accessing `/`, you need to connect to the actual endpoints as defined in the .yaml files in the openapi/ folder.
* You can access the Swagger UI to debug the endpoints by adding a /ui at the end of each API's base url
* Examples:
  * http://0.0.0.0:9090/v1.0/ui
  * http://0.0.0.0:9090/oim/v0.2/ui
* The webserver runs on unencrypted HTTP locally to avoid added complexity of SSL/TLS. Generally the apiserver is expected to be run behind a reverse-proxy like nginx. More on that in the docker-compose chapter.

## Testing

Test-cases are defined in in test.py for now. 

You can manually run the test suite by calling `python test.py`

The recommended IDE (vscode) and mentioned extensions provide better test integration however.


## Examples

### DB Order Request Body
```json
{
  "items": [
    {
      "deputy-id": "b123456",
      "deputy-mail": "b123456@js.on",
      "owner-id": "b123456",
      "owner-mail": "b123456@js.on",
      "sbu": "BE",
      "catalog-reference": "PGSQL01",
      "size": "S1",
      "metal-category": "B",
      "environment": "Test",
      "security-zone": "_Z1",
      "group-permissions": [
        {
          "ad-group-name": "f_adm",
          "local-group-name": "wheel"
        }
      ],
      "data-disk": {
        "filesystem": "/data",
        "size-gb": 1
      }
    }
  ],
  "requester-id": "b123456"
}
```
### JBoss Order Request Body
```json
{
  "items": [
    {
      "catalog-reference": "MP03",
      "data-disk": {
        "filesystem": "/data",
        "size-gb": 1
      },
      "deputy-id": "b123456",
      "environment": "Dev",
      "group-permissions": [
        {
          "ad-group-name": "f_adm",
          "local-group-name": "wheel"
        }
      ],
      "metal-category": "B",
      "owner-id": "b123456",
      "security-zone": "PROD",
      "size": "S1",
      "version": 7.1
    }
  ],
  "requester-id": "b123456",
  "sbu": "BE"
}
```

### Linux Order Request Body
```json
{
  "items": [
    {
      "catalog-reference": "L01",
      "metal-class": "B",
      "environment": "Test",
      "security-zone": "PROD",
      "role": "APP",
      "size": "S1",
      "owner-id": "b123456",
      "deputiy-id": "b123456",
      "group-permissions": [
        {
          "ad-group-name": "f_adm",
          "local-group-name": "wheel"
        }
      ],
      "data-disk": {
        "filesystem": "/opt",
        "size-gb": 1
      }
    }
  ],
  "requester-id": "b123456",
  "sbu": "BE"
}
```

### Windows Order Request Body
```json
{
  "items": [
    {
      "catalog-reference": "W01",
      "metal-class": "B",
      "environment": "Test",
      "security-zone": "PROD",
      "role": "APP",
      "size": "S1",
      "owner-id": "b123456",
      "deputiy-id": "b123456",
      "group-permissions": [
        {
          "ad-group-name": "f_adm",
          "local-group-name": "Users"
        }
      ],
      "data-disk": {
        "filesystem": "D",
        "size-gb": 1
      }
    }
  ],
  "requester-id": "b123456",
  "sbu": "BE"
}
```
