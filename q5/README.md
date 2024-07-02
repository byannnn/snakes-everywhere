# Solution Overview

I made the following assumptions for the solution to question 5:
- Users are allowed to login from any country, as long as they provide a valid country code.
- Country codes should work in any case (upper or lower).
- Usernames and passwords of any length are allowed (a very bad idea, but validation is straightforward to implement for serious usecases).
- HTTP error code 403 will be returned for invalid country codes.
- HTTP error code 401 will be returned for invalid username/passwords.

I used `fastapi_template` (https://github.com/s3rius/FastAPI-template) to generate the boilerplate code used for this solution.

For encryption, I used `bcrypt` library.

For DB, I used `sqlite3` as it is the most simple and straightforward DB to set up and prototype with. If this is to be used in a production environment, perhaps MariaDB would be a better fit.

The solution _does_ include proper alembic migrations, but this should be unneeded. I did not test it due to lack of time :(, but I provided a backup DB that is pre-populated with the proper schema and country codes, under `<root>/question_5/sqlite.db.backup`. Please feel free to use it.

Other stacks used:
- Poetry
- SQLAlchemy

`.gitignore` is auto-generated.

Docker containerization is supposedly available out-of-the-box with `fastapi_template`, but I did not test it.

# Usage

All Python dependencies are captured in `requirements.txt`, but please follow usage instructions below instead (smoother and faster process).

To setup and run the API (working directory should be the directory that contains `alembic.ini` and the `.env` files):
```
pip install bcrypt poetry
poetry install
poetry run python -m question_5
```

The default URL of the hosted API is at: `http://127.0.0.1:8000`.

The swagger documentation can be found at `/api/docs`, so `http://127.0.0.1:8000/api/docs`.

The authentication function is located at `/api/auth` as a POST request, so `http://127.0.0.1:8000/api/auth`.

I created an API call to register users at `/api/register` to simplify user creation, so `http://127.0.0.1:8000/api/register`.

# Others

The list of country codes I used to populate my DB with is from here: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
