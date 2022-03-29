# GEOWebsite

Website for the Global Education Observatory platform. Built with Django 4 on Python 3.9. HTML template is [Editorial by HTML5 UP](https://html5up.net/editorial). Integrates with W&M CAS for authentication using [django-cas-ng](https://pypi.org/project/django-cas-ng/). Serves static files using [whitenoise](https://pypi.org/project/whitenoise/). Any pushes to `main` branch is mirrored to an internal repo at <https://code.wm.edu>, which builds a Docker container using the Dockerfile and uploads it to the W&M Docker registry. Updates get picked up from the registry and become live at <https://geo.ds.wm.edu> within a few minutes.

## Development

- Clone this repo
- Create a Python 3.9 virtual environment with `python -m venv .venv`.
- Activate the venv
  - Windows/Powershell: `.venv/Scripts/Activate.ps1`
  - Linux/Most shells: `source .venv/bin/activate`
- Install requirements with `pip install -r requirements.txt`
  - Note: `mysqlclient` may require additional steps to get to build. Linux should have `default-libmysqlclient-dev`, `build-essential`, and `python3-dev` or `python3.9-dev` depending on system Python install. Windows should choose a `mysqlclient` version with prebuilt binaries. See <https://pypi.org/project/mysqlclient/>.
- [Optional] Install eslint and prettier with `npm install` for Javascript linting and formatting
- Set up the following environment variables:
  - `DEBUG` Set to `true` for testing. Enables the debug sidebar and outputs stacktrace to the browser. Set to `false` for production. Defaults to `true`.
    - Note: These are all-lowercase strings.
  - `SECRET_KEY` Long random string used to add entropy to cryptography. Not required when testing.
  - `DB_NAME` Name of the table (production), or full path of the sqlite file (test)
  - `DB_ENGINE` Use `django.db.backends.mysql` (production) or `django.db.backends.sqlite3` (test). Note that SQLite does not support spatial data types by default.
  - `DB_USER` Username for MySQL. Not used for SQLite.
  - `DB_PASSWORD` Password for MySQL. Not used for SQLite.
  - `DB_HOST` Address of the MySQL server. Not used for SQLite.
    - Note: The production MySQL server is on an internal network and will not accept outside connections. To access it for local development, you will need to use an SSH tunnel through a trusted machine.
  - `DB_PORT` Port of the MySQL server. Not used for SQLite. Use `3306`.
  - `CAS_SERVER_URL` URL of the W&M CAS server. Use `https://cas.wm.edu/cas/`.
  - Tip: Set up these variables in a shell script, then you can just run `source envs.sh` to add all of them at once.
- Start the development server with `python cms/manage.py runserver 8080`
  - Note: Local port must be 8080 or W&M CAS will reject authentication requests.