from pydantic import ValidationError
import pytest
import pandas as pd
import json
from common_feature import LABEL_ORDER
from predict import process_input, model_predict
from predict import InferencePayload

# Define paths to the test JSON files
TEST_SINGLE_FALSE = "tests/test_single_false.json"
TEST_SINGLE_MTRUE = "tests/test_single_mtrue.json"


@pytest.fixture
def example_payload():
    """Return the example payload from InferencePayload schema_extra."""
    return InferencePayload.Config.json_schema_extra["example"]


@pytest.fixture
def test_payload_false():
    """Load the test_single_false.json file."""
    with open(TEST_SINGLE_FALSE, "r") as f:
        return json.load(f)


@pytest.fixture
def test_payload_mtrue():
    """Load the test_single_mtrue.json file."""
    with open(TEST_SINGLE_MTRUE, "r") as f:
        return json.load(f)


def test_schema_validation(example_payload):
    """Test that the example payload conforms to the schema."""
    try:
        payload = InferencePayload(**example_payload)
        assert payload.Statement == example_payload["Statement"]
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e}")


def test_process_input(example_payload):
    """Test that process_input correctly transforms the input."""
    payload = InferencePayload(**example_payload)
    X_input, true_label = process_input(payload)

    # Ensure the transformation returns a DataFrame
    assert isinstance(X_input, pd.DataFrame)
    assert not X_input.empty

    # Ensure the true label is extracted correctly
    assert true_label == example_payload["Label"]


def test_predict_single_false(test_payload_false):
    """Test prediction on test_single_false.json."""
    payload = InferencePayload(**test_payload_false)
    X_input, true_label = process_input(payload)

    # Make prediction
    predicted_label = model_predict(X_input)

    # Ensure the prediction is a valid label
    assert predicted_label in LABEL_ORDER

    assert (predicted_label == true_label) is True


def test_predict_single_mtrue(test_payload_mtrue):
    """Test prediction on test_single_mtrue.json."""
    payload = InferencePayload(**test_payload_mtrue)
    X_input, true_label = process_input(payload)

    # Make prediction
    predicted_label = model_predict(X_input)

    # Ensure the prediction is a valid label
    assert predicted_label in LABEL_ORDER

    assert (predicted_label == true_label) is True
