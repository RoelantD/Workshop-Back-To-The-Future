import argparse, joblib, pandas as pd, json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

TARGET = "HomeResult"

def main(data_path: str, out_dir: str = "model"):
    print("Starting model training...\nDepending on your hardware, this can take 0-4 minutes. Please wait...", flush=True)
    if not Path(data_path).exists():
        print(f"ERROR: Data file not found: {data_path}", flush=True)
        exit(1)
    print("Loading data...", flush=True)
    df = pd.read_csv(data_path)
    assert TARGET in df.columns, f"Missing target '{TARGET}'"
    exclude_cols = [TARGET, "Winner", "HomeScore", "AwayScore", "NumberOfSpectators"]
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    categorical_cols = [c for c in feature_cols if df[c].dtype == 'object' or str(df[c].dtype).startswith('bool')]
    numeric_cols = [c for c in feature_cols if c not in categorical_cols]

    print("Preparing features and target...", flush=True)
    X = df[feature_cols]
    y = df[TARGET].astype(str)

    print("Splitting data into train and test sets...", flush=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Building preprocessing pipelines...", flush=True)
    numeric_pipe = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler(with_mean=False))])
    categorical_pipe = Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])

    preprocess = ColumnTransformer([("num", numeric_pipe, numeric_cols), ("cat", categorical_pipe, categorical_cols)])

    print("Training model (this may take a while)...", flush=True)
    model = Pipeline([("preprocess", preprocess), ("clf", LogisticRegression(max_iter=500))])
    model.fit(X_train, y_train)

    print("Evaluating model...", flush=True)
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}", flush=True)
    print(classification_report(y_test, y_pred), flush=True)

    print("Saving model and schema...", flush=True)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, Path(out_dir) / "home_result_model.joblib")
    schema = {"feature_cols": feature_cols, "categorical_cols": categorical_cols, "numeric_cols": numeric_cols, "target": TARGET, "classes_": sorted(y.unique().tolist())}
    (Path(out_dir) / "schema.json").write_text(json.dumps(schema, indent=2))

    print(f"Model and schema saved to: {out_dir}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="datasets/football-results.csv")
    parser.add_argument("--out_dir", default="model")
    args = parser.parse_args()
    main(args.data, args.out_dir)
