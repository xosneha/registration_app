# Registration App

Full-stack application providing user login/registration functionality.

## Pre-requisites

1. Ensure docker is installed.

## Instructions to run

1. Navigate into the `docker` directory and copy `sample.env` into `.env`.
2. Fill out the missing values for `.env`.
3. Run `docker compose up --build -d`.
4. By default, the frontend will run on `http://localhost:80`.

> **NOTE** If the application is being deployed, then `typescript/registration_app/.env` should be updated to point to the public IP.
