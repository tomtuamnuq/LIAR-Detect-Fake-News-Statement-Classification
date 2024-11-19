import pandas as pd
import pickle
from xgboost import XGBClassifier
import os

from common_feature import COLUMN_NAMES, FeatureEngineer

# File paths
DATA_DIR = os.path.join(os.pardir, "data")
MODEL_DIR = os.path.join(os.pardir, "models")
TRAIN_FILE = os.path.join(DATA_DIR, "train.tsv")
TEST_FILE = os.path.join(DATA_DIR, "test.tsv")


# Main Script
def main():
    # Load data
    train_df = pd.read_csv(TRAIN_FILE, sep="\t", header=None)
    test_df = pd.read_csv(TEST_FILE, sep="\t", header=None)
    train_df.columns = COLUMN_NAMES
    test_df.columns = COLUMN_NAMES

    # Combine datasets for consistent preprocessing
    combined_df = pd.concat([train_df, test_df], axis=0)

    # Data cleaning
    combined_df = combined_df[combined_df.isnull().sum(axis=1) <= 3].copy()
    categorical_column_names = combined_df.select_dtypes(
        include=["object"]
    ).columns.tolist()
    combined_df[categorical_column_names] = combined_df[
        categorical_column_names
    ].fillna("unknown")

    # Feature engineering
    feature_engineer = FeatureEngineer()
    X_combined = feature_engineer.assemble_training_features(combined_df)
    y_combined = feature_engineer.encode_target(combined_df)

    # Train the XGBoost model
    model = XGBClassifier(eval_metric="mlogloss", random_state=42)
    model.fit(X_combined, y_combined)

    # Save the model and encoders
    with open(os.path.join(MODEL_DIR, "feature_engineer.pkl"), "wb") as f:
        pickle.dump(feature_engineer, f)
    with open(os.path.join(MODEL_DIR, "xgboost_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    print("Feature Engineer and Model saved successfully!")


if __name__ == "__main__":
    main()
