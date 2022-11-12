import json
import os
from datetime import date, timedelta

import requests

from .cache import r
from .exceptions import AvailabilityAPIException

CALENDARIFIC_API_KEY = os.environ["CALENDARIFIC_API_KEY"]


def _make_holidays_request(params: dict) -> dict:
    """Execute the request to fetch the holidays to the calendarific API.
    This function must receive the a dict that will contain two required keys:
    `country` and `year` that later will be joined with the api_key to send
    the request.

    :param params: A dict of params for the request.
    :type params: dict
    :return: The dict with the parsed JSON of the response.
    :rtype: dict
    """
    response = requests.get(
        "https://calendarific.com/api/v2/holidays?",
        params={"api_key": CALENDARIFIC_API_KEY, **params},
    )
    data = json.loads(response.text)
    if response.status_code != 200:
        if "error" not in data:
            data["error"] = "Unknown error with holidays API."
        raise AvailabilityAPIException(data["error"])
    return data["response"]["holidays"]


def _get_holidays(country: str, year: int) -> list:
    """
    Get the holidays for a given country and
    year using the calendarific API or the redis cache.

    This method will cache the results using redis since this info will be
    updated quarterly and we dont want to fetch the data again without changes.

    :param country: The country code. Example: US
    :type country: str
    :param year: The year used to search the holidays. Example 2022
    :type year: int
    :return: The list of holidays for that country in that year.
    :rtype: list
    """
    cache_key_name = f"{country}-{year}"
    cached_holidays = r.get(cache_key_name)
    if cached_holidays is None:
        holidays = _make_holidays_request(
            {
                "country": country,
                "year": year,
            }
        )
        r.setex(cache_key_name, timedelta(days=1), json.dumps(holidays))
    else:
        holidays = json.loads(cached_holidays.decode())

    return holidays


def is_holiday(date_iso: str, country: str) -> bool:
    """Given a date and country, this function determines
    whether the date provided is holiday or not.

    :param date: The date to check.
    :type date: str
    :param country: The corresponding country.
    :type country: str
    :return: Whether it is holiday or not.
    :rtype: bool
    """
    holidays = _get_holidays(country, date.fromisoformat(date_iso).year)
    holidays_iso_dates = [h["date"]["iso"] for h in holidays]
    return date_iso in holidays_iso_dates
