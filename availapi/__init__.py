import pytz
from flask import Flask, abort, jsonify, make_response, request
from webargs.flaskparser import use_args

from .exceptions import AvailabilityAPIException
from .holidays import is_holiday
from .schemas import RangeSchema, SlotSchema

app = Flask(__name__)


@app.route("/availability-check", methods=["POST"])
@use_args(RangeSchema(many=True), location="json")
def check_availability(data):

    # First we validate something that we could not validate on marshmallow.
    if len(data) == 0:
        abort(422, "Invalid input type. The array is empty.")

    # Step 1: Convert all datetimes to UTC.
    utc_dt_ranges = []
    for dt_range in data:
        utc_from_dt = pytz.utc.normalize(dt_range["from_datetime"])
        utc_to_dt = pytz.utc.normalize(dt_range["to_datetime"])
        utc_dt_ranges.append(
            {"from_datetime": utc_from_dt, "to_datetime": utc_to_dt}
        )

    # Step 2: Find the highest `from` datetime as our `from` candidate.
    from_dt_candidate = max(
        *[utc_dt_range["from_datetime"] for utc_dt_range in utc_dt_ranges]
    )

    # Step 3: Find the lowest `to` datetime as our `to` candidate.
    to_dt_candidate = min(
        *[utc_dt_range["to_datetime"] for utc_dt_range in utc_dt_ranges]
    )

    if from_dt_candidate >= to_dt_candidate:
        # Then there is not a slot when all ranges be intercepted.
        abort(
            400, "There were not slots available where all this ranges match."
        )
    else:
        slot_json = SlotSchema().dump(
            [
                {
                    "from_datetime": from_dt_candidate,
                    "to_datetime": to_dt_candidate,
                }
            ],
            many=True,
        )

    return make_response(slot_json, 200, {"Content-Type": "application/json"})


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


# Return validation errors as JSON
@app.errorhandler(422)
@app.errorhandler(400)
def handle_errors(err):
    if err.code == 422:
        if hasattr(err, "data"):
            # Entering here meaning that the error was generated by marshmallow.
            errors_data = err.data["messages"]
        else:
            # Otherwise was a message generated from the flask.abort function.
            errors_data = {"json": {"_schema": [err.description]}}
    elif err.code == 400:
        errors_data = err.description
    return jsonify({"errors": errors_data}), err.code
