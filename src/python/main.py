# # src/python/main.py
# import os
# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LogisticRegression

# # Set data directory from environment variable for Docker compatibility
# DATA_DIR = os.getenv("DATA_DIR", "src/data")  # ./src/data for local runs
# train_path = os.path.join(DATA_DIR, "train.csv")

# # Load training data
# print(f"[INFO] Loading train.csv from: {train_path}")
# train_df = pd.read_csv(train_path)
# print(f"[INFO] Train shape: {train_df.shape}")

import os
import sys
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# --- Config: where to find the CSVs ---
DATA_DIR = os.getenv("DATA_DIR", "src/data")  # default for local runs
TRAIN = os.path.join(DATA_DIR, "train.csv")
TEST  = os.path.join(DATA_DIR, "test.csv")

def log(msg):
    print(f"[INFO] {msg}", flush=True)

def ensure_file(path, name):
    if not os.path.exists(path):
        log(f"ERROR: {name} not found at {path}")
        sys.exit(1)

def main():
    # ------------------------------------------------------------
    # 13) Load train.csv
    # ------------------------------------------------------------
    ensure_file(TRAIN, "train.csv")
    log(f"Loading train.csv from: {TRAIN}")
    train = pd.read_csv(TRAIN)
    log(f"Train shape: {train.shape}")

    # ------------------------------------------------------------
    # 14) Explore / add / adjust (lightweight prints + chosen features)
    # ------------------------------------------------------------
    log("Preview (first 5 rows):")
    log(train.head(5).to_string(index=False))

    # Basic exploration summaries
    log("Column summary:")
    log(train.dtypes.to_string())
    log("Missing values (top few):")
    log(train.isna().sum().sort_values(ascending=False).head(10).to_string())

    # We'll use a very simple feature set: Sex (categorical) and Age (numeric)
    features = ["Sex", "Age"]
    target = "Survived"
    log(f"Selected features: {features}")
    log(f"Target: {target}")

    # ------------------------------------------------------------
    # Simple preprocessing:
    # - Age: impute missing with median
    # - Sex: one-hot encode (handle unknown just in case)
    # ------------------------------------------------------------
    numeric_features = ["Age"]
    categorical_features = ["Sex"]

    numeric_pipe = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="median"))
    ])
    categorical_pipe = Pipeline(steps=[
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_features),
            ("cat", categorical_pipe, categorical_features),
        ]
    )

    # ------------------------------------------------------------
    # 15) Logistic Regression model on training set
    # ------------------------------------------------------------
    model = Pipeline(steps=[
        ("prep", preprocessor),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    X_train = train[features].copy()
    y_train = train[target].astype(int).copy()

    log("Fitting logistic regression (features: Sex, Age)")
    model.fit(X_train, y_train)
    log("Model fit complete.")

    # Coefficients (optional: show transformed feature names)
    try:
        oh = model.named_steps["prep"].named_transformers_["cat"].named_steps["onehot"]
        cat_names = oh.get_feature_names_out(categorical_features)
        all_names = np.concatenate([numeric_features, cat_names])
        coefs = model.named_steps["clf"].coef_.ravel()
        coef_table = pd.DataFrame({"feature": all_names, "coef": coefs})
        log("Model coefficients:\n" + coef_table.to_string(index=False))
    except Exception as e:
        log(f"(Skipping coef printout: {e})")

    # ------------------------------------------------------------
    # 16) Training accuracy
    # ------------------------------------------------------------
    y_pred_train = model.predict(X_train)
    train_acc = accuracy_score(y_train, y_pred_train)
    log(f"Training accuracy: {train_acc:.4f}")

    # ------------------------------------------------------------
    # 17) Load test.csv & predict on test set
    # ------------------------------------------------------------
    ensure_file(TEST, "test.csv")
    log(f"Loading test.csv from: {TEST}")
    test = pd.read_csv(TEST)
    log(f"Test shape: {test.shape}")

    # Keep just the columns we need (others may exist)
    if not set(features).issubset(test.columns):
        missing = list(set(features) - set(test.columns))
        log(f"ERROR: test.csv is missing required columns: {missing}")
        sys.exit(1)

    X_test = test[features].copy()
    log("Predicting on test set...")
    test_preds = model.predict(X_test)

    # ------------------------------------------------------------
    # 18) Test accuracy (if labels exist), otherwise useful prints
    # ------------------------------------------------------------
    if "Survived" in test.columns:
        y_test = test["Survived"].astype(int)
        test_acc = accuracy_score(y_test, test_preds)
        log(f"Test accuracy: {test_acc:.4f}")
    else:
        # Kaggle test.csv typically lacks labels
        log("Test accuracy: N/A (no Survived column in test.csv).")
        log(f"Predicted survival rate on test: {test_preds.mean():.3f}")
        log("First 10 predictions: " + np.array2string(test_preds[:10], separator=","))

    # (Optional) Save a submission-style CSV if PassengerId exists
    if "PassengerId" in test.columns:
        out_path = os.path.join(DATA_DIR, "submission.csv")
        pd.DataFrame({
            "PassengerId": test["PassengerId"],
            "Survived": test_preds.astype(int)
        }).to_csv(out_path, index=False)
        log(f"Saved predictions to: {out_path}")

    log("Done.")

if __name__ == "__main__":
    main()
