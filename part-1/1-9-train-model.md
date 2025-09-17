# Step-by-Step Workshop: Building the Model Training Script (`train.py`)

This workshop will guide you through constructing a machine learning training script step by step. By the end, you'll have a complete [`train.py`](./code/train.py) that loads data, preprocesses it, trains a model, evaluates it, and saves the results.

---

## 1. Introduction & Requirements

We'll use Python and several popular libraries, all specified in the provided `requirements.txt` file.

**Install requirements:**
```bash
pip install -r part-1/code/requirements.txt
```

---

## 2. Loading the Data


👉 **Build Along:**
Open a new file called `train.py` in your `code` folder. In this step, add the code to load the dataset using pandas. Run your script to check that the data loads and prints the first few rows.

First, let's load the dataset using pandas.

```python
import pandas as pd

df = pd.read_csv('datasets/football-results.csv')
print(df.head())
```

**Explanation:**
- We import pandas and read the CSV file into a DataFrame.
- `print(df.head())` shows the first few rows to verify loading.

---

## 3. Selecting Features and Target


👉 **Build Along:**
Now, in your `train.py`, add code to select the target column and define your feature columns. Print out the list of features and the shape of your data to check your work.

Identify which columns to use as features and which as the target variable.


```python
TARGET = "HomeResult"
exclude_cols = [TARGET]  # You may want to add more columns here!
feature_cols = [c for c in df.columns if c not in exclude_cols]
X = df[feature_cols]
y = df[TARGET].astype(str)
```


**Explanation:**
- We set the target column and, by default, only exclude the target itself from the features.
- `feature_cols` contains the names of the input features.
- `X` is the feature matrix, `y` is the target vector.

---

### 📝 Exercise: Feature Selection and Data Leakage


👉 **Build Along:**
Experiment with the `exclude_cols` list in your script. Try including or excluding different columns and see how it affects your features. Discuss or note your findings.

Take a look at the columns in your dataset. Which columns do you think should be included as features, and which should be excluded? Write down your thoughts and try different options in your code.

- What makes a column a good feature for predicting the target?
- Are there columns that would "leak" the answer (i.e., give away the target directly)?
- What would happen if you included columns like `Winner`, `HomeScore`, or `AwayScore` when predicting `HomeResult`?

**Suggestion:**
- Try adding columns such as `Winner`, `HomeScore`, or `AwayScore` to the `exclude_cols` list above and see how it affects your model's performance.

**Note:**
- Including columns like `Winner` or the actual scores would make the model's job trivial, as these columns are directly related to the target and would result in data leakage. This would lead to unrealistically high accuracy during training, but the model would not generalize to new, real-world data where these values are not known in advance.

---

### 📝 Exercise: Feature Selection and Data Leakage

Take a look at the columns in your dataset. Which columns do you think should be included as features, and which should be excluded? Discuss with your group or write down your thoughts.

- What makes a column a good feature for predicting the target?
- Are there columns that would "leak" the answer (i.e., give away the target directly)?
- What would happen if you included columns like `Winner`, `HomeScore`, or `AwayScore` when predicting `HomeResult`?

**Discussion:**
- Including columns like `Winner` or the actual scores would make the model's job trivial, as these columns are directly related to the target and would result in data leakage. This would lead to unrealistically high accuracy during training, but the model would not generalize to new, real-world data where these values are not known in advance.

**Experiment:**
- Try changing the `exclude_cols` list and see how it affects your model's performance. What happens if you include or exclude different columns?

---

## 4. Splitting the Data


👉 **Build Along:**
Add the code to split your data into training and test sets. Print the shapes of your splits to confirm the operation worked as expected.

Split the data into training and test sets.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Explanation:**
- We use `train_test_split` to create training and test sets.
- `test_size=0.2` means 20% of the data is used for testing, 80% for training.
- `random_state=42` ensures reproducibility (you get the same split every time).
- `stratify=y` keeps the class distribution the same in both sets (important for classification problems).

---

## 5. Preprocessing Pipelines

👉 **Build Along:**
Add the code for preprocessing pipelines to your script. Start by identifying your categorical and numeric columns, then build the pipelines and the `ColumnTransformer`. Print out the pipeline objects to check your setup.

Before we dive in: Building these pipelines might look complex at first glance, but it's not as hard as it seems! With a few lines of code, you can handle a lot of data preparation automatically. And hey—it’s not called Data Science without good reason. 😄

---

### Why do we need to process data?

Raw data is rarely perfect for machine learning. It may contain missing values, inconsistent formats, or features on very different scales. Processing ("preprocessing") the data helps:
- Fill in or handle missing values
- Convert categories to numbers
- Make sure all features are on a similar scale
- Remove irrelevant or problematic columns

This makes the data easier for the model to learn from and improves results.

---

### Removing columns with too many missing values


👉 **Build Along:**
If your dataset has columns with many missing values (like `NumberOfSpectators`), add code to drop them before building your pipelines.

Sometimes a column has so many missing values that it's better to remove it entirely. In our dataset, `NumberOfSpectators` often contains null values. Let's remove it before building the pipeline:

```python
if 'NumberOfSpectators' in df.columns:
	df = df.drop(columns=['NumberOfSpectators'])
```

---

**What do 'impute' and 'scale' mean?**
- **Impute:** This means filling in missing values in your data. For example, if a column has some empty cells, the imputer can fill them with the median (for numbers) or the most common value (for categories).
- **Scale:** This means adjusting numeric values so they're on a similar scale. For example, if one feature is in the range 0-1 and another is 0-1000, scaling helps the model treat them fairly.

Handle missing values, scale numeric features, and encode categorical features using pipelines.

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

categorical_cols = [c for c in feature_cols if df[c].dtype == 'object' or str(df[c].dtype).startswith('bool')]
numeric_cols = [c for c in feature_cols if c not in categorical_cols]

numeric_pipe = Pipeline([
	("impute", SimpleImputer(strategy="median")),
	("scale", StandardScaler(with_mean=False)),
])
categorical_pipe = Pipeline([
	("impute", SimpleImputer(strategy="most_frequent")),
	("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocess = ColumnTransformer([
	("num", numeric_pipe, numeric_cols),
	("cat", categorical_pipe, categorical_cols),
])
```

**Explanation:**
- Numeric features are imputed and scaled.
- Categorical features are imputed and one-hot encoded.
- `ColumnTransformer` applies the correct pipeline to each column type.

---

## 6. Building the Model Pipeline


👉 **Build Along:**
Add the code to create your model pipeline by combining the preprocessing and the classifier. Print the pipeline to verify.

Combine preprocessing and model training into a single pipeline.

```python
from sklearn.linear_model import LogisticRegression

model = Pipeline([
	("preprocess", preprocess),
	("clf", LogisticRegression(max_iter=500)),
])
```

**Explanation:**
- The pipeline first preprocesses the data, then fits a logistic regression classifier.

---

## 7. Training the Model


👉 **Build Along:**
Now, fit your model pipeline to the training data. Print a message when training starts and ends so you know this step is running.


To train ("fit") the model, we provide it with examples of input data (`X_train`) and the correct answers (`y_train`). The model uses these to learn patterns and relationships, so it can make accurate predictions on new, unseen data. `X_train` contains the features for each training example, while `y_train` contains the corresponding labels or targets.

Fit the model to the training data.

```python
model.fit(X_train, y_train)
```

**Explanation:**
- The pipeline handles all preprocessing and model fitting in one step.

---

## 8. Evaluating the Model


👉 **Build Along:**
Add code to evaluate your model on the test set. Print the accuracy and classification report. Try changing your features and see how the results change.

Check the model's performance on the test set.

```python
from sklearn.metrics import classification_report, accuracy_score

y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred))
```


**Explanation:**
- We print the accuracy and a detailed classification report.

---

### Interpreting Model Evaluation Results

After training, you'll see metrics like accuracy, precision, recall, and F1-score. Here's what they mean:

- **Accuracy:** The percentage of correct predictions. Higher is generally better, but can be misleading if classes are imbalanced.
- **Precision:** Of all the times the model predicted a class, how often was it correct? High precision means few false positives.
- **Recall:** Of all the actual cases of a class, how many did the model find? High recall means few false negatives.
- **F1-score:** The harmonic mean of precision and recall. A good balance between the two.

**What is good?**
- For a balanced dataset, look for high values (close to 1.0) for all metrics, especially for the classes you care about most.
- If one class is much more important, focus on its precision/recall/F1.
- If accuracy is very high but precision/recall are low for some classes, your model may be missing important cases.

**Tip:**
- Always compare your results to a simple baseline (like always guessing the most common class). If your model is only a little better, try improving your features or model.

---

## 9. Saving the Model and Schema


👉 **Build Along:**
Finally, add code to save your trained model and the schema to disk. Check that the files are created in your output directory.

Save the trained model and schema for later use.

```python
import joblib, json
from pathlib import Path

Path("model").mkdir(parents=True, exist_ok=True)
joblib.dump(model, Path("model") / "home_result_model.joblib")
schema = {
	"feature_cols": feature_cols,
	"categorical_cols": categorical_cols,
	"numeric_cols": numeric_cols,
	"target": TARGET,
	"classes_": sorted(y.unique().tolist()),
}
(Path("model") / "schema.json").write_text(json.dumps(schema, indent=2))
```

**Explanation:**
- The model is saved with joblib.
- The schema (feature info) is saved as JSON.

---


You now have a robust, reusable training script for your machine learning workflow!

---

When you finish each step, run your script to check your progress. If you get stuck, look at the complete example in the code folder: [`train.py`](./code/train.py).

---

## 🚀 What's Next?

Now that you've built and saved your own machine learning model, it's time to make it useful! In the next section, you'll learn how to deploy your model by adding an API and connecting it to an AI agent. This will allow you (and others) to interact with your model programmatically and unlock its full potential.

Get ready to bring your model to life!

[⏮️ Previous](/part-1/1-8-transformers.md) 
[⏭️ Next](/part-1/1-10-deploy-model.md)