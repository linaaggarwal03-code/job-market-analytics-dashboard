"""
ml_model.py
----------------
A small but genuinely-trained machine learning component: a Random Forest
regressor that predicts salary_in_usd from job/company attributes.

This is intentionally kept simple (no hyperparameter search, no external
model registry) because the goal is to demonstrate a clean, correct,
end-to-end ML pipeline -- not to win a Kaggle competition. The pipeline
(preprocessing + model) is what you'd want to point to in an interview:
it handles categorical encoding properly, splits data for honest
evaluation, and reports uncertainty instead of just a single number.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

NUMERIC_FEATURES = ["work_year"]
CATEGORICAL_FEATURES = [
    "experience_level",
    "employment_type",
    "job_title",
    "remote_ratio",
    "company_location",
    "company_size",
]
TARGET = "salary_in_usd"

# Job titles that appear fewer than this many times get bucketed into
# "Other" before one-hot encoding. Without this, a handful of one-off
# titles (e.g. a title that appears once) would each become their own
# sparse column and add noise without adding predictive power.
MIN_JOB_TITLE_COUNT = 5


@dataclass
class ModelResult:
    """Bundles everything app.py needs to use and explain the trained model."""

    pipeline: Pipeline
    r2: float
    mae: float
    n_train: int
    n_test: int
    job_titles: list[str]
    countries: list[str]


def _bucket_rare_job_titles(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["job_title"].value_counts()
    common_titles = counts[counts >= MIN_JOB_TITLE_COUNT].index
    df = df.copy()
    df["job_title"] = df["job_title"].where(df["job_title"].isin(common_titles), "Other")
    return df


@st.cache_resource(show_spinner=False)
def train_salary_model(df: pd.DataFrame) -> ModelResult:
    """
    Train a Random Forest salary predictor on the (unfiltered) dataset.

    Cached with st.cache_resource since the trained model is a Python
    object (not plain data) that should persist across reruns -- retraining
    on every filter change would make the predictor tab feel sluggish for
    no benefit, since the model is intentionally trained on the *full*
    dataset regardless of sidebar filters.
    """
    model_df = _bucket_rare_job_titles(df)

    X = model_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = model_df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=200,
                    max_depth=12,
                    min_samples_leaf=3,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)

    return ModelResult(
        pipeline=pipeline,
        r2=r2,
        mae=mae,
        n_train=len(X_train),
        n_test=len(X_test),
        job_titles=sorted(model_df["job_title"].unique().tolist()),
        countries=sorted(model_df["company_location"].unique().tolist()),
    )


def predict_salary(
    result: ModelResult,
    work_year: int,
    experience_level: str,
    employment_type: str,
    job_title: str,
    remote_ratio: str,
    company_location: str,
    company_size: str,
) -> tuple[float, float]:
    """
    Predict salary_in_usd for a single hypothetical job, plus an uncertainty
    estimate.

    The uncertainty is the standard deviation of predictions across the
    Random Forest's individual trees -- a simple but legitimate way to turn
    an ensemble model into something that communicates "how confident is
    this guess", rather than a single misleadingly-precise number.
    """
    input_row = pd.DataFrame(
        [
            {
                "work_year": work_year,
                "experience_level": experience_level,
                "employment_type": employment_type,
                "job_title": job_title,
                "remote_ratio": remote_ratio,
                "company_location": company_location,
                "company_size": company_size,
            }
        ]
    )

    pipeline = result.pipeline
    preprocessed = pipeline.named_steps["preprocess"].transform(input_row)
    forest: RandomForestRegressor = pipeline.named_steps["model"]

    tree_preds = np.array([tree.predict(preprocessed)[0] for tree in forest.estimators_])

    return float(tree_preds.mean()), float(tree_preds.std())
