from datetime import date

import pytz
from flask import Flask, abort, make_response
from webargs.flaskparser import use_args

from .core.error_handler import configure_error_handlers
from .core.schemas import RangeSchema, SlotSchema
from .docs.spec import generate_spec_json, spec
from .docs.swagger import swaggerui_blueprint
from .utils.holidays import is_holiday
from .utils.weekends import is_weekend

app = Flask(__name__)


def _validate_special_dates(d: date, cc: str):
    """Check whether the date given correspond to a weekend or holiday.

    :param d: The date to check.
    :type d: date
    :param cc: The corresponding country.
    :type cc: str
    """
    base_error_message = "Unable to find an available slot."
    if is_weekend(d):
        abort(
            400,
            f"{base_error_message} The date {d.isoformat()} correspond "
            "to a weekend.",
        )

    if is_holiday(d, cc):
        abort(
            400,
            f"{base_error_message} The date {d.isoformat()} is "
            f"holiday in {cc}.",
        )


@app.route("/availability-check", methods=["POST"])
@use_args(RangeSchema(many=True), location="json")
def check_availability_endpoint(data):
    """Check availability view.
    ---
    post:
      summary: Check availability
      description: |
        Determine and returns a meeting slot available (in UTC) between an
        array of object that individually represent certain availability range
        in a given country.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items: RangeSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: array
                items: SlotSchema
        400:
          $ref: '#/components/responses/BadRequest'
        422:
          $ref: '#/components/responses/UnprocessableEntity'
      tags:
        - Availability
    """
    # First we validate something that we could not validate on marshmallow.
    if len(data) == 0:
        abort(422, "Invalid input type. The array is empty.")

    # Step 1: Check all datetimes to validate and normalize.
    utc_dt_ranges = []
    for dt_range in data:
        # Step 1.1: Validate whether some date is holiday or weekend.
        _validate_special_dates(
            dt_range[
                "from_datetime"  # "to_datetime" would have worked too.
            ].date(),
            dt_range["cc"],
        )

        # Step 1.2: Normalize the dates to UTC timezone.
        utc_from_dt = pytz.utc.normalize(dt_range["from_datetime"])
        utc_to_dt = pytz.utc.normalize(dt_range["to_datetime"])
        utc_dt_ranges.append(
            {"from_datetime": utc_from_dt, "to_datetime": utc_to_dt}
        )

    if len(utc_dt_ranges) == 1:
        # Edge case: What if only a single range is sent?
        from_dt_candidate = utc_dt_ranges[0]["from_datetime"]
        # The max/min functions has a wrong behavior with a one datetime item.
        to_dt_candidate = utc_dt_ranges[0]["to_datetime"]
    else:
        # Step 2: Find the highest `from` datetime as our `from` candidate.
        from_dt_candidate = max(
            *[utc_dt_range["from_datetime"] for utc_dt_range in utc_dt_ranges]
        )

        # Step 3: Find the lowest `to` datetime as our `to` candidate.
        to_dt_candidate = min(
            *[utc_dt_range["to_datetime"] for utc_dt_range in utc_dt_ranges]
        )

    if from_dt_candidate >= to_dt_candidate:
        # Then there is not a slot when all ranges are intercepted.
        abort(
            400,
            "There were no slots available where all these ranges matched.",
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


# Documentation configuration
with app.test_request_context():
    spec.path(view=check_availability_endpoint)
app.add_url_rule("/spec.json", "spec", generate_spec_json)
app.register_blueprint(swaggerui_blueprint)

# Error handler configuration
configure_error_handlers(app)
