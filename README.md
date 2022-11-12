# Availability API

## Introduction
Working internationally comes with its own set of challenges, among them the challenge of figuring out when people are available.

Availability API is a REST API that can be used to calculate the best meeting slots across time zones.

## Getting started

#### Prerequisites
- Clone the repository.
- Make sure that docker and docker compose are installed on your machine.

#### Usage
In order to run this API and see how it works, you need to run the following command:
`docker-compose up -d` or `docker compose up -d` (if you are using the `compose` plugin).

The API should be available now in the following host: `http://localhost:3000`.

#### Docs
A swagger documentation is available in `http://localhost:3000/docs`.

#### Development (optional)
1. Make sure you have Python 3.x installed on your machine.
2. Create and activate a [virtual env](https://docs.python.org/3/library/venv.html#creating-virtual-environments).
3. Install the requirements on `requirements.txt` (`pip3 install -r requirements.txt`).
4. Create your `.env` file (you can use the default values in the `.env.example`).
5. Make sure your PostgreSQL and Redis services are running and that you placed the correct values on the `.env` including the database you will use.
6. Run the migrations `flask db upgrade head`.
7. Start the API in development mode `flask run`.
8. To execute the **tests** you can use the following command: `pytest`.
