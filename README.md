# Availability API (availapi)

## Introduction
Working internationally comes with its own set of challenges, among them the challenge of figuring out when people are available.

Availability API is a REST API that can be used to calculate the best meeting slots across time zones.

## Usage (local environment)

### Prerequisites
- Clone the repository.
- Make sure that docker and docker compose are installed on your machine.

### How to start the API?
In order to run this API and see how it works, you need to run the following command:
`docker-compose up --build` or `docker compose up --build` (if you are using the `compose` plugin).

The API should be available now in the following host: `http://localhost:5000`.
### Docs
A swagger documentation is available in [http://localhost:5000/docs](http://localhost:5000/docs).

## Definitions and assumptions
### How it works?
This API has one endpoint that is `POST http://localhost:5000/availability-check`. This endpoint receives an array of hashes in a JSON body and returns a JSON array with the slots availables in **UTC**. More details format can be found in the documentation.

The input array of hashes represent a list with all the ranges that the endpoint needs to consider to calculate a slots available.

Prior the calculus, we check whether the input data correspond to a weekend day or a holiday for a given country and if so we return an error that explain that such day is unable to be used to find a meeting slot.

### Limitations
The individual array items needs to correspond to a single day, so basically if you need to check the availability of two days, you would need to make two API calls: The first with the range for one day and the second with the range of the other day.

### DST
DST is supported since our input already will take an datetime that include a timezone offset.

### Technical decisions
- **Language:** Python.
- **Framework:** Flask.
- **Holidays validation:** Calendarific API + Redis for cache the holidays for a given country. I decided to use an API since it is better to outsource the maintenance of the holidays for all countries to a third party api than have to take care by my own in my 2-days operations.
- **Country codes validation:** Dictionary with all the countries supported, this is hardcoded due the low probability that can be changed. This was taken directly from the calendarific API, maybe i could cache it also on redis however i felt that it was less probable to change so i hardcoded it.
- **Documentation:** Swagger UI blueprint.
- **Timezone library:** `pytz` library due the simplicity and readibility that it adds when manipulating timezones common operations.

## Tests

In order to run the tests, run the following command:
`docker-compose up --build availapi-tests` or `docker compose up --build availapi-tests` (if you are using the `compose` plugin).

## Development (optional)
1. Make sure you have Python 3.x installed on your machine.
2. Create and activate a [virtual env](https://docs.python.org/3/library/venv.html#creating-virtual-environments).
3. Install the requirements on `requirements.txt` (`pip3 install -r requirements.txt`).
4. Create your `.env` file (you can use the default values in the `.env.example`).
5. Make sure your Redis service is running and that you placed the correct values on the `.env` including the database you will use.
6. Start the API in development mode `flask --debug run`.
7. To execute the **tests** you can use the following command: `python3 -m pytest`.

