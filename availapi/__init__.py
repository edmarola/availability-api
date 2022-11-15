import pytz
from flask import Flask, abort, jsonify, make_response, request
from webargs.flaskparser import use_args

from .core.error_handler import configure_error_handlers
from .core.exceptions import AvailabilityAPIException
from .core.schemas import RangeSchema, SlotSchema
from .docs.spec import generate_spec_json, spec
from .docs.swagger import swaggerui_blueprint
from .utils.holidays import is_holiday

app = Flask(__name__)


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


# Documentation configuration
with app.test_request_context():
    spec.path(view=check_availability_endpoint)
app.add_url_rule("/spec.json", "spec", generate_spec_json)
app.register_blueprint(swaggerui_blueprint)

# Error handler configuration
configure_error_handlers(app)
