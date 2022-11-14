from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)

from availapi.utils.countries import supported_countries


class RangeSchema(Schema):
    from_datetime = fields.AwareDateTime(
        required=True,
        data_key="from",
        metadata={
            "description": "`From` datetime for an individual availability."
        },
    )
    to_datetime = fields.AwareDateTime(
        required=True,
        data_key="to",
        metadata={
            "description": "`To` datetime for an individual availability."
        },
    )
    cc = fields.Str(
        required=True,
        validate=validate.OneOf(supported_countries.keys()),
        metadata={
            "description": "Country code of an individual. "
            "Must be on iso-3166 format."
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
    from_datetime = fields.AwareDateTime(
        required=True,
        data_key="from",
        # format="%Y-%m-%dT%H:%M:%S.%fZ",
        format="%Y-%m-%dT%H:%M:%S.0Z",
        metadata={"description": "`From` datetime for a given meeting slot."},
    )
    to_datetime = fields.AwareDateTime(
        required=True,
        data_key="to",
        # format="%Y-%m-%dT%H:%M:%S.%fZ",
        format="%Y-%m-%dT%H:%M:%S.0Z",
        metadata={"description": "`To` datetime for a given meeting slot."},
    )
