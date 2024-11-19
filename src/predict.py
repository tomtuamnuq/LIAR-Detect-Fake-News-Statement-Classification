import os
import pickle
import pandas as pd
import json

from xgboost import XGBClassifier

from common_feature import LABEL_ORDER, FeatureEngineer


TEST_DIR = os.path.join(os.pardir, "test")
MODEL_DIR = os.path.join(os.pardir, "models")
# File paths
TEST_FILE = os.path.join(TEST_DIR, "test_single_mtrue.json")

# Load the model and feature engineer
with open(os.path.join(MODEL_DIR, "feature_engineer.pkl"), "rb") as f:
    feature_engineer: FeatureEngineer = pickle.load(f)

with open(os.path.join(MODEL_DIR, "xgboost_model.pkl"), "rb") as f:
    model: XGBClassifier = pickle.load(f)

# Read the single JSON input file
with open(TEST_FILE, "r") as f:
    single_input = json.load(f)

print(f"Predicting: {single_input}")
# Convert JSON input to DataFrame
input_df = pd.DataFrame([single_input])

# Preprocess the input using the feature engineer
X_input = feature_engineer.transform(input_df)
print(f"Converted as: {X_input}")

# Predict the label
predicted_label_idx = model.predict(X_input)[0]
predicted_label = LABEL_ORDER[predicted_label_idx]

# Log the result
print(f"Predicted label: {predicted_label}")
