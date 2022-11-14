from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_dump,
    validate,
    validates_schema,
)

from availapi.utils.countries import supported_countries


class RangeSchema(Schema):
    from_datetime = fields.AwareDateTime(
        required=True,
        data_key="from",
        metadata={
            "description": "`From` datetime for an individual availability. "
            "Must be on RFC 3339 format and include the timezone offset.",
            "example": "2022-11-02T09:00:00.0+08:00",
        },
    )
    to_datetime = fields.AwareDateTime(
        required=True,
        data_key="to",
        metadata={
            "description": "`To` datetime for an individual availability. "
            "Must be on RFC 3339 format and include the timezone offset.",
            "example": "2022-11-02T17:00:00.0+08:00",
        },
    )
    cc = fields.Str(
        required=True,
        validate=validate.OneOf(supported_countries.keys()),
        metadata={
            "description": "Country code for an item. "
            "Must be on iso-3166 format.",
            "example": "SG",
        },
    )

    @validates_schema
    def check_from_to_relation(self, data, **kwargs):
        """
        Check that the `from_datetime` be always a past datetime in regards to
        the `to_datetime`.
        """
        if data["from_datetime"] > data["to_datetime"]:
            raise ValidationError(
                "The `from` field must be a past "
                "date in regards to the `to` field."
            )


class SlotSchema(Schema):
    from_datetime = fields.DateTime(
        required=True,
        data_key="from",
        format="%Y-%m-%dT%H:%M:%S.%f",
        metadata={
            "description": "`From` datetime for a given meeting slot.",
            "example": "2022-11-02T01:00:00.0Z",
        },
    )
    to_datetime = fields.DateTime(
        required=True,
        data_key="to",
        format="%Y-%m-%dT%H:%M:%S.%f",
        metadata={
            "description": "`To` datetime for a given meeting slot.",
            "example": "2022-11-02T09:00:00.0Z",
        },
    )

    @post_dump
    def format_microseconds(self, data, **kwargs):
        """
        Format correctly the microseconds to keep it with only one digit
        and also put the Z (we are sure at this point that they are in UTC).

        """
        data["from"] = data["from"][:-5] + "Z"
        data["to"] = data["to"][:-5] + "Z"
        return data
