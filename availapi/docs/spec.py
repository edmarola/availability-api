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

spec.components.schema(
    "UnprocessableEntityA",
    {
        "type": "object",
        "properties": {
            "error": {
                "type": "object",
                "properties": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "<n>": {
                                "type": "object",
                                "properties": {
                                    "<field_name>": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "example": "Missing data "
                                            "for required field.",
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
            }
        },
        "example": {
            "errors": {
                "json": {
                    "0": {"cc": ["Missing data for required field."]},
                    "2": {"to": ["Missing data for required field."]},
                }
            }
        },
    },
)

spec.components.schema(
    "UnprocessableEntityB",
    {
        "type": "object",
        "properties": {
            "error": {
                "type": "object",
                "properties": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "_schema": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "example": "Invalid input type.",
                                },
                            }
                        },
                    }
                },
            }
        },
        "example": {"errors": {"json": {"_schema": ["Invalid input type."]}}},
    },
)

spec.components.response(
    "UnprocessableEntity",
    {
        "description": "Unprocessable Entity",
        "content": {
            "application/json": {
                "schema": {
                    "oneOf": [
                        {"$ref": "#/components/schemas/UnprocessableEntityA"},
                        {"$ref": "#/components/schemas/UnprocessableEntityB"},
                    ]
                },
            },
        },
    },
)


def generate_spec_json():
    return jsonify(spec.to_dict())
