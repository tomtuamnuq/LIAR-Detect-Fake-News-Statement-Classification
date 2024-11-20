from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError, Field
from typing import Optional
import pandas as pd
import pickle
from xgboost import XGBClassifier
from common_feature import (
    FEATUREENGINEER_FILE,
    LABEL_ORDER,
    MODEL_FILE,
    FeatureEngineer,
)

# Flask app
app = Flask(__name__)


# Load the model and feature engineer
with open(FEATUREENGINEER_FILE, "rb") as f:
    feature_engineer: FeatureEngineer = pickle.load(f)

with open(MODEL_FILE, "rb") as f:
    model: XGBClassifier = pickle.load(f)


# Define schema for the input payload using pydantic
class InferencePayload(BaseModel):
    ID: Optional[str] = Field(None, description="Unique ID for the statement")
    Label: Optional[str] = Field(
        None, description="True label, if known, for validation"
    )
    Statement: str = Field(..., description="The statement to be classified")
    Subject: str = Field(
        ..., description="Comma-separated list of subjects related to the statement"
    )
    Speaker: str = Field(..., description="Name of the speaker")
    Speaker_Job_Title: Optional[str] = Field(
        None, description="Job title of the speaker"
    )
    State_Info: Optional[str] = Field(
        None, description="State information related to the statement"
    )
    Party_Affiliation: str = Field(
        ..., description="Political party affiliation of the speaker"
    )
    Barely_True_Counts: int = Field(
        ..., ge=0, description="Count of 'barely true' statements"
    )
    False_Counts: int = Field(..., ge=0, description="Count of 'false' statements")
    Half_True_Counts: int = Field(
        ..., ge=0, description="Count of 'half true' statements"
    )
    Mostly_True_Counts: int = Field(
        ..., ge=0, description="Count of 'mostly true' statements"
    )
    Pants_on_Fire_Counts: int = Field(
        ..., ge=0, description="Count of 'pants on fire' statements"
    )
    Context: Optional[str] = Field(
        None, description="Context of the statement (e.g., debate, speech)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "ID": "12996",
                "Label": "pants-fire",
                "Statement": "The number of illegal immigrants could be 3 million. It could be 30 million.",
                "Subject": "immigration",
                "Speaker": "donald-trump",
                "Speaker_Job_Title": "President-Elect",
                "State_Info": "New York",
                "Party_Affiliation": "republican",
                "Barely_True_Counts": 63,
                "False_Counts": 114,
                "Half_True_Counts": 51,
                "Mostly_True_Counts": 37,
                "Pants_on_Fire_Counts": 61,
                "Context": "a speech in Phoenix, Ariz.",
            }
        }


def process_input(payload):
    """
    Convert JSON payload into a DataFrame and preprocess using FeatureEngineer.

    Parameters:
    - payload (dict): JSON payload received via REST API.

    Returns:
    - X_input (pd.DataFrame): Transformed input ready for model inference.
    - true_label (str or None): True label if provided in the input, else None.
    """
    true_label = payload.Label
    input_df = pd.DataFrame([payload.model_dump()])
    X_input = feature_engineer.transform(input_df)
    return X_input, true_label


def model_predict(X_input: pd.DataFrame):
    # Predict using the model
    predicted_label_idx = model.predict(X_input)[0]
    predicted_label = LABEL_ORDER[predicted_label_idx]
    return predicted_label


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle POST requests for inference. Accepts JSON payload, performs inference, and returns prediction.
    """
    # Parse and validate JSON payload using pydantic
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400
    try:
        data = InferencePayload(**payload)
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    try:
        # Process input and extract true label
        X_input, true_label = process_input(data)
        predicted_label = model_predict(X_input)

        # Prepare response
        response = {"predicted_label": predicted_label}

        if true_label:
            response["true_label"] = true_label
            response["correct"] = predicted_label == true_label

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5042, debug=True)
