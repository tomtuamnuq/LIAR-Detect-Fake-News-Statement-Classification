# Define column names
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# File paths
# Get the absolute path of the current directory (where common_feature.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths relative to the src directory
DATA_DIR = os.path.join(BASE_DIR, "../data")
MODEL_DIR = os.path.join(BASE_DIR, "../models")
TRAIN_FILE = os.path.join(DATA_DIR, "train.tsv")
TEST_FILE = os.path.join(DATA_DIR, "test.tsv")
FEATUREENGINEER_FILE = os.path.join(MODEL_DIR, "feature_engineer.pkl")
MODEL_FILE = os.path.join(MODEL_DIR, "xgboost_model.pkl")

COLUMN_NAMES = [
    "ID",
    "Label",
    "Statement",
    "Subject",
    "Speaker",
    "Speaker_Job_Title",
    "State_Info",
    "Party_Affiliation",
    "Barely_True_Counts",
    "False_Counts",
    "Half_True_Counts",
    "Mostly_True_Counts",
    "Pants_on_Fire_Counts",
    "Context",
]

NUMERICAL_FEATURES = [
    "Barely_True_Counts",
    "False_Counts",
    "Half_True_Counts",
    "Mostly_True_Counts",
    "Pants_on_Fire_Counts",
]

LABEL_ORDER = [
    "true",
    "mostly-true",
    "half-true",
    "barely-true",
    "false",
    "pants-fire",
]


# Feature Engineering Class
class FeatureEngineer:
    def __init__(self):  # TODO hyperparameter optimization of the feature engineering
        self.min_freq = 150
        self.subject_encoder = MultiLabelBinarizer(sparse_output=False)
        self.included_subjects = None
        self.top_n_categories = 5
        self.speaker_encoder = OneHotEncoder(
            handle_unknown="ignore", sparse_output=False
        )
        self.party_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.statement_vectorizer = TfidfVectorizer(
            stop_words="english", max_df=0.7, max_features=100, strip_accents="ascii"
        )
        self.context_vectorizer = TfidfVectorizer(
            stop_words="english", max_df=0.7, max_features=50, strip_accents="ascii"
        )
        self.feature_names = {}

    @staticmethod
    def get_subject_list(subject: str):
        return [s.strip().lower() for s in subject.split(",")]

    def _create_unique_feature_names(self, col, variants):
        feature_names = [f"{col}_{feat}" for feat in variants]
        self.feature_names[col] = feature_names
        return feature_names

    def filter_subjects(self, subject_lists):
        return subject_lists.apply(
            lambda subject_list: [
                s for s in subject_list if s in self.included_subjects
            ]
        )

    def fit_subject_column(self, df):
        subject_lists = df["Subject"].apply(self.get_subject_list)
        # Count subject frequencies in training data
        all_subjects = [subject for subjects in subject_lists for subject in subjects]
        subject_counts = pd.Series(all_subjects).value_counts()

        # exclude rare subjects
        self.included_subjects = set(
            subject_counts[subject_counts >= self.min_freq].index
        )
        subject_lists = self.filter_subjects(subject_lists)
        transformed = self.subject_encoder.fit_transform(subject_lists)
        feature_names = self._create_unique_feature_names(
            "Subject", self.subject_encoder.classes_
        )
        return pd.DataFrame(
            transformed,
            columns=feature_names,
            index=df.index,
        )

    def fit_categorical_column(self, col, df, encoder):
        top_items = set(df[col].value_counts().nlargest(self.top_n_categories).index)
        df[col] = df[col].apply(lambda x: x if x in top_items else "Other")
        transformed = encoder.fit_transform(df[[col]])
        feature_names = self._create_unique_feature_names(
            col, encoder.get_feature_names_out([col])
        )
        return pd.DataFrame(
            transformed,
            columns=feature_names,
            index=df.index,
        )

    def fit_text_column(self, col, df, vectorizer):
        transformed = vectorizer.fit_transform(df[col])
        feature_names = self._create_unique_feature_names(
            col, vectorizer.get_feature_names_out()
        )
        return pd.DataFrame(
            transformed.toarray(),  # sparse -> dense
            columns=feature_names,
            index=df.index,
        )

    def assemble_training_features(self, df):
        return pd.concat(
            [
                df[NUMERICAL_FEATURES],
                self.fit_subject_column(df),
                self.fit_categorical_column("Speaker", df, self.speaker_encoder),
                self.fit_categorical_column(
                    "Party_Affiliation", df, self.party_encoder
                ),
                self.fit_text_column("Statement", df, self.statement_vectorizer),
                self.fit_text_column("Context", df, self.context_vectorizer),
            ],
            axis=1,
        )

    @staticmethod
    def encode_target(df):
        label_mapping = {label: idx for idx, label in enumerate(LABEL_ORDER)}
        return df["Label"].map(label_mapping)

    def transform(self, df: pd.DataFrame):
        """
        Transforms new data using the fitted encoders and vectorizers.

        Parameters:
        - df (pd.DataFrame): Input DataFrame with a single row of data for inference.

        Returns:
        - pd.DataFrame: Transformed DataFrame ready for model input.
        """
        # Ensure the Subject column uses the fitted encoder and filters based on `included_subjects`
        subject_lists = df["Subject"].apply(self.get_subject_list)
        subject_lists = self.filter_subjects(subject_lists)
        transformed_subjects = self.subject_encoder.transform(subject_lists)
        subject_features = pd.DataFrame(
            transformed_subjects,
            columns=self.feature_names["Subject"],
            index=df.index,
        )

        # Transform categorical columns using fitted encoders
        speaker_features = pd.DataFrame(
            self.speaker_encoder.transform(df[["Speaker"]]),
            columns=self.feature_names["Speaker"],
            index=df.index,
        )

        party_features = pd.DataFrame(
            self.party_encoder.transform(df[["Party_Affiliation"]]),
            columns=self.feature_names["Party_Affiliation"],
            index=df.index,
        )

        # Transform text columns using fitted vectorizers
        statement_features = pd.DataFrame(
            self.statement_vectorizer.transform(df["Statement"]).toarray(),
            columns=self.feature_names["Statement"],
            index=df.index,
        )
        context_features = pd.DataFrame(
            self.context_vectorizer.transform(df["Context"]).toarray(),
            columns=self.feature_names["Context"],
            index=df.index,
        )

        # Combine all features into a single DataFrame
        return pd.concat(
            [
                df[NUMERICAL_FEATURES],
                subject_features,
                speaker_features,
                party_features,
                statement_features,
                context_features,
            ],
            axis=1,
        )
