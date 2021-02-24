# ChemReg 2.0 REST API

Chemical Curation and Data Management

# Developer Setup

## Required software

You'll need the following software installed on your machine to begin development.

* [Python 3.8](https://www.python.org/downloads/) or [Conda](https://www.anaconda.com/distribution/#download-section)
* [Git](https://git-scm.com/downloads)
* [Docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/) (see [Deploying with Docker page](https://github.com/Chemical-Curation/chemcurator_django/wiki/Deploying-with-Docker))

## Running chemreg

Open up a terminal or command prompt for the following.

#### 1. Clone the chemreg_django repository and enter into the downloaded directory.

```bash
git clone https://github.com/Chemical-Curation/chemcurator_django.git
cd chemcurator_django
```

#### 2. Create your Python virtual environment.

Python 3.8 - Linux and macOS:
```bash
python3.8 -m venv .venv
source .venv/bin/activate
```
Python 3.8 - Windows:
```bash
python3.8 -m venv .venv
.venv\Scripts\activate.bat
```

Conda - Linux and macOS:
```bash
conda create -n chemreg python=3.8
source activate chemreg
```

Conda - Windows:
```bash
conda create -n chemreg python=3.8
activate chemreg
```

#### 3. Install requirements.

##### 3.0 - Install pre-requirements.

If you are on Windows, you will likely need the Microsoft Visual C++ 14.0 [build tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16)
* Selecting the C++ libraries from the installer will be sufficient to build the python environment.

![build_tools](https://user-images.githubusercontent.com/7052993/75799083-63a62b00-5d2c-11ea-8b83-976110af880b.PNG)

##### 3.1 - Install requirements.
Install the Python requirements from the file w/in the `/chemcurator_django` repository:
```bash
pip install -r requirements.txt
```

#### 4. Edit your configuration.

Make a copy of the "template.env" file and name it ".env". Change the uncommented attribute in `.env` to hold the following:
* Set `DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/chemreg`

*Note: A line in your .env preceded by "#" will be ignored.*

#### 5. Launch Docker services.

*Note: These may take a while the first time you run them.*

##### On linux/macOS you can use these commands, using the `chemcurator_default` network...

```bash
docker run \
    --volume=postgresql:/var/lib/postgres/data \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=chemreg \
    --name=postgresql \
    --network=chemcurator_default \
    --publish "5432:5432" \
    --detach \
    postgres:12.1
```

```bash
docker run \
    --volume=pgadmin4:/var/lib/pgadmin \
    -e "PGADMIN_DEFAULT_EMAIL=dev@epa.gov" \
    -e "PGADMIN_DEFAULT_PASSWORD=postgres" \
    -e "PGADMIN_LISTEN_PORT=5047" \
    --name=pgadmin4 \
    --network=chemcurator_default \
    --publish="5432:5432" \
    --detach \
    dpage/pgadmin4
```
> Note: When adding a server to pgadmin4, use the postgres container name `postgresql` instead of `localhost`

##### On windows you can use these commands, using the network created...

```bash
docker network create --driver=bridge pgnetwork
```

```bash
docker run --publish 5432:5432 --volume=postgresql:/var/lib/postgres/data -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=chemreg --name=postgresql --network=pgnetwork --detach postgres:12.1
```

```bash
docker run --publish 5047:80 --volume=pgadmin4:/var/lib/pgadmin -e "PGADMIN_DEFAULT_EMAIL=dev@epa.gov" -e "PGADMIN_DEFAULT_PASSWORD=postgres" --name=pgadmin4 --network=pgnetwork --detach dpage/pgadmin4
```

#### 6. Install the git hook scripts.

This will initialize your git repository to run the `.pre-commit-config.yaml` whenever you go to commit changes.

```bash
pre-commit install
```

#### 7. Migrate the database and start the runserver.

```bash
python manage.py migrate
```
*Note: The variable `URL_CONF` variable in the .env file can be set to show `admin` or `api` urls. Be sure to set it appropriately before starting up the runserver.*

For example, to run the API on port 8000 and the admin application on 8001:

```bash
python manage.py runserver 8000
```
(macOS syntax)
```bash
URL_CONF=admin python manage.py runserver 8001
```

(Windows syntax)
```bash
set URL_CONF=admin 
```
or 
```
$env:URL_CONF = 'admin'
```
Then
```
python manage.py runserver 8001
```
#### 8. Inspect.

You can now go to your browser and visit `http://127.0.0.1:8000/` to see what the runserver is serving. And for to inspect the DB with the PGAdmin4 container visit `http://localhost:5047/` and when prompted to sign in use the variables entered above when starting the container which are:
* Email Address : `dev@epa.gov`
* Password : `postgres`
You can then right-click on "Servers" on the left and then provide a name in the "General" tab and then use the credentials used in the docker container
* Host : if using host network `localhost` ; if using pgnetwork `postgresql`
* Username : `postgres`
* Password : `postgres`

![create_db_server](https://user-images.githubusercontent.com/7052993/75771757-76eed180-5cff-11ea-9d93-effa863e2c7a.png)



# Finishing up your code changes

#### 1. Lint your code.

We follow a code-style defined by the default settings of [`black`](https://github.com/psf/black). It automatically formats your code. The [`isort`](https://github.com/timothycrosley/isort) package handles the structure of imports in `.py` files. [`flake8`](https://gitlab.com/pycqa/flake8) is used for PEP8 compliance. Tests will fail if this is not done. To format your code changes, run:

```bash
python manage.py lint
```
*Note: The pre-commit hooks installed above will prevent a commit before this is done if any formatting is needed.*

#### 2. Build documentation
We use the [Google style-guide](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for docstrings. Try to write good docstrings as you write functions.

The `sphinx-autoapi` package automatically crawls the source code and outputs the docs. 

To build the documentation: 
```bash
cd docs/
sphinx-build -b html . _build
```
