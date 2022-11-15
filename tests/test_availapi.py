ENDPOINT_URL = "/availability-check"


def test_sc1_happy_path(client):
    """
    Scenario 1: Happy path
    Given three ranges, a valid time slot in UTC must be returned.
    """
    # Arrange
    request_body = [
        {
            "from": "2022-05-02T09:00:00.0+08:00",
            "to": "2022-05-02T17:00:00.0+08:00",
            "cc": "SG",
        },
        {
            "from": "2022-05-02T09:00:00.0+01:00",
            "to": "2022-05-02T17:00:00.0+01:00",
            "cc": "NG",
        },
        {
            "from": "2022-05-02T09:00:00.0+05:30",
            "to": "2022-05-02T17:00:00.0+05:30",
            "cc": "IN",
        },
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 200, "The status must be 200."
    assert response.is_json, "The response format must be JSON."
    assert response.json == [
        {"from": "2022-05-02T08:00:00.0Z", "to": "2022-05-02T09:00:00.0Z"}
    ], "The output did not match."


def test_sc2_empty_input(client):
    """
    Scenario 2: Empty input
    Given an empty array, an error message must be returned.
    """
    # Arrange
    request_body = []

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 422, "The status must be 422."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": {
            "json": {"_schema": ["Invalid input type. The array is empty."]}
        }
    }, "The output did not match."


def test_sc3_from_to_inverted(client):
    """
    Scenario 3: From/To inverted
    Given a range with a from/to inverted, an error must be returned.
    """
    # Arrange
    request_body = [
        {
            "from": "2022-05-02T17:00:00.0+08:00",
            "to": "2022-05-02T09:00:00.0+08:00",
            "cc": "SG",
        },
        {
            "from": "2022-05-02T09:00:00.0+01:00",
            "to": "2022-05-02T17:00:00.0+01:00",
            "cc": "NG",
        },
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 422, "The status must be 422."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": {
            "json": {
                "0": {
                    "_schema": [
                        "The `from` field must be a past date"
                        " in regards to the `to` field."
                    ]
                }
            }
        }
    }, "The output did not match."


def test_sc4_range_missing_keys(client):
    """
    Scenario 4: Range missing keys
    Given ranges with missing keys, an error must be returned.
    """
    # Arrange
    request_body = [
        {
            "from": "2022-05-02T17:00:00.0+08:00",
            "cc": "SG",
        },
        {
            "to": "2022-05-02T17:00:00.0+01:00",
        },
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 422, "The status must be 422."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": {
            "json": {
                "0": {"to": ["Missing data for required field."]},
                "1": {
                    "cc": ["Missing data for required field."],
                    "from": ["Missing data for required field."],
                },
            }
        }
    }, "The output did not match."


def test_sc5_missing_body(client):
    """
    Scenario 5: Missing body
    Given a request with a missing body, an error must be returned.
    """
    # Act
    response = client.post(ENDPOINT_URL)

    # Assert
    assert response.status_code == 422, "The status must be 422."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": {"json": {"_schema": ["Invalid input type."]}}
    }, "The output did not match."


def test_sc6_field_values_format_error(client):
    """
    Scenario 6: Field values with format error
    Given all the required field with format errors, an error is returned.
    """
    # Arrange
    request_body = [
        {"from": "", "to": "2022-05-02T17:00:00.000+08:00", "cc": "ZZ"}
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 422, "The status must be 422."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": {
            "json": {
                "0": {
                    "cc": [
                        "Must be one of: AF, AL, DZ, AS, AD, AO, AI, AG, AR, "
                        "AM, AW, AU, AT, AZ, BH, BD, BB, BY, BE, BZ, BJ, BM, "
                        "BT, BO, BA, BW, BR, VG, BN, BG, BF, BI, CV, KH, CM, "
                        "CA, KY, CF, TD, CL, CN, CO, KM, CG, CD, CK, CR, CI, "
                        "HR, CU, CW, CY, CZ, DK, DJ, DM, DO, TL, EC, EG, SV, "
                        "GQ, ER, EE, ET, FK, FO, FJ, FI, FR, PF, GA, GM, GE, "
                        "DE, GH, GI, GR, GL, GD, GU, GT, GG, GN, GW, GY, HT, "
                        "HN, HK, HU, IS, IN, ID, IR, IQ, IE, IM, IL, IT, JM, "
                        "JP, JE, JO, KZ, KE, KI, XK, KW, KG, LA, LV, LB, LS, "
                        "LR, LY, LI, LT, LU, MO, MG, MW, MY, MV, ML, MT, MH, "
                        "MQ, MR, MU, YT, MX, FM, MD, MC, MN, ME, MS, MA, MZ, "
                        "MM, NA, NR, NP, NL, NC, NZ, NI, NE, NG, KP, MK, MP, "
                        "NO, OM, PK, PW, PA, PG, PY, PE, PH, PL, PT, PR, QA, "
                        "RE, RO, RU, RW, SH, KN, LC, MF, PM, VC, WS, SM, ST, "
                        "SA, SN, RS, SC, SL, SG, SX, SK, SI, SB, SO, ZA, KR, "
                        "SS, ES, LK, BL, SD, SR, SE, CH, SY, TW, TJ, TZ, TH, "
                        "BS, TG, TO, TT, TN, TR, TM, TC, TV, VI, UG, UA, AE, "
                        "GB, US, UY, UZ, VU, VA, VE, VN, WF, YE, ZM, ZW, SZ."
                    ],
                    "from": ["Not a valid datetime."],
                }
            }
        }
    }, "The output did not match."


def test_sc7_three_items_without_slot(client):
    """
    Scenario 7: Three items without slot available
    Given three ranges not intercepted, an meaningful response is returned.
    """
    # Arrange
    request_body = [
        {
            "from": "2022-05-02T09:00:00.0-06:00",
            "to": "2022-05-02T17:00:00.0-06:00",
            "cc": "MX",
        },
        {
            "from": "2022-05-02T09:00:00.0+01:00",
            "to": "2022-05-02T17:00:00.0+01:00",
            "cc": "NG",
        },
        {
            "from": "2022-05-02T09:00:00.0+05:30",
            "to": "2022-05-02T17:00:00.0+05:30",
            "cc": "IN",
        },
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 400, "The status must be 400."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": "There were not slots available "
        "where all this ranges match."
    }, "The output did not match."


def test_sc8_usa_holiday(client):
    """
    Scenario 8: Range including a holiday.
    Given two ranges with one USA holiday, a meaningful response is returned.
    """
    # Arrange
    request_body = [
        {
            "from": "2022-12-23T09:00:00.0-06:00",
            "to": "2022-12-23T17:00:00.0-06:00",
            "cc": "MX",
        },
        {
            "from": "2022-12-23T09:00:00.0-05:00",
            "to": "2022-12-23T17:00:00.0-05:00",
            "cc": "US",
        },
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 400, "The status must be 400."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": "Unable to find an available slot. "
        "The date 2022-12-23 is holiday on US."
    }, "The output did not match."


def test_sc9_single_range(client):
    """
    Scenario 9: Single range scenario
    Given a single range, return the availability corresponding to that range.
    """

    # Arrange
    request_body = [
        {
            "from": "2022-05-02T09:00:00.0+08:00",
            "to": "2022-05-02T17:00:00.0+08:00",
            "cc": "SG",
        }
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 200, "The status must be 200."
    assert response.is_json, "The response format must be JSON."
    assert response.json == [
        {"from": "2022-05-02T01:00:00.0Z", "to": "2022-05-02T09:00:00.0Z"}
    ], "The output did not match."


def test_sc11_usa_weekend(client):
    """
    Scenario 11: Range including a weekend.
    Given two ranges with one weekend, a meaningful response is returned.
    """
    # Arrange
    request_body = [
        {
            "from": "2022-12-24T09:00:00.0-06:00",
            "to": "2022-12-24T17:00:00.0-06:00",
            "cc": "MX",
        },
        {
            "from": "2022-12-24T09:00:00.0-05:00",
            "to": "2022-12-24T17:00:00.0-05:00",
            "cc": "US",
        },
    ]

    # Act
    response = client.post(ENDPOINT_URL, json=request_body)

    # Assert
    assert response.status_code == 400, "The status must be 400."
    assert response.is_json, "The response format must be JSON."
    assert response.json == {
        "errors": "Unable to find an available slot. "
        "The date 2022-12-24 correspond to a weekend."
    }, "The output did not match."
