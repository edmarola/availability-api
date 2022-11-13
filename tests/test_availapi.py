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
    assert response.json == {"error": {}}, "The output did not match."


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
    assert response.json == {"error": {}}, "The output did not match."


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
    assert response.json == {"error": {}}, "The output did not match."


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
    assert response.json == {"error": {}}, "The output did not match."
