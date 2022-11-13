from flask import Flask, abort, jsonify, request

from .exceptions import AvailabilityAPIException
from .holidays import is_holiday

app = Flask(__name__)


@app.route("/is_holiday")
def is_holiday_service():
    cc = request.args["cc"]
    date = request.args["date"]

    try:
        if is_holiday(date, cc):
            response = jsonify("Holiday")
        else:
            response = jsonify("Not holiday")

    except AvailabilityAPIException as e:
        abort(500, str(e))

    return response
