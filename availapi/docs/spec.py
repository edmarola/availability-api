from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import jsonify

spec = APISpec(
    title="AvailAPI",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="REST API that allows to calculate the best available "
        "match between several availability ranges with different offset."
    ),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.response(
    "BadRequest",
    {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "string",
                            "example": "There were not slots available "
                            "where all this ranges match.",
                        },
                    },
                },
            }
        },
    },
)

spec.components.response(
    "UnprocessableEntity",
    {
        "description": "Unprocessable Entity",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "object",
                            "example": [
                                {
                                    "json": {
                                        "0": {
                                            "cc": [
                                                "Missing data for required field."
                                            ]
                                        },
                                        "2": {
                                            "to": [
                                                "Missing data for required field."
                                            ]
                                        },
                                    }
                                },
                                {"json": {"_schema": ["Invalid input type."]}},
                            ],
                        },
                    },
                },
            }
        },
    },
)


def generate_spec_json():
    return jsonify(spec.to_dict())
