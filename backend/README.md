# Backend

## Getting started

Note: run the commands (esp. `python3 -m venv .venv` if using MacOS) in the root of the project instead of in `/backend`. This is to make sure IDE picks up the Python Virtual Environment.

### MacOS (with Homebrew)

#### Prerequisites

```bash
brew install \
  python3 \
  mysql \
  pkg-config
```

#### Create a virtual environment

```bash
python3 -m venv .venv
```

#### Create and start the local database

```bash
brew services start mysql
mysql -u root -p
```

```sql
CREATE DATABASE <whatever_you_want>;
```

```bash
quit (to exit mysql)
```

#### Set up environment variables

```bash
cp backend/.env.example backend/.env
```

...and edit the `backend/.env` file with your local MySQL connection details

#### Install backend dependencies

```bash
. .venv/bin/activate
pip install -r backend/requirements.txt
```

#### Run the backend locally (in venv)

At least once to create the tables:

```bash
python3 backend/app.py
```

After that, flask command can be used:

```bash
flask --app backend/app.py run
```

#### Run API tests

```bash
pytest -v
```
