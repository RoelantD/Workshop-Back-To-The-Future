# Top Machine Learning Algorithms for Prediction

## 1️⃣ Linear Regression
### Type: Regression
**Linear regression** is one of the simplest and most interpretable algorithms. It models the relationship between a dependent variable and one or more independent variables by fitting a linear equation.

```
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train) 
```

**Pros:**
- Easy to implement and interpret
- Works well for linearly related data

**Cons:**  
- Assumes linearity  
- Sensitive to outliers  

## 2️⃣ Logistic Regression
### Type: Classification
**Logistic regression** is a classification algorithm despite its name. It models the probability that a given input belongs to a particular class.

```
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
```

**Pros:**
- Interpretable
- Efficient on linearly separable data

**Cons:**
- Limited to binary or multi-class classification
- Assumes linear decision boundary

## 3️⃣ Decision Trees
### Type: Classification and Regression
**Decision trees** split data based on feature values to form a tree-like structure. They are intuitive and can capture non-linear relationships.

```
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
```

**Pros:**
- Easy to visualize
- Handles both numerical and categorical data

**Cons:**
- Prone to overfitting
- Unstable to small data variations

## 4️⃣ Random Forest
### Type: Classification and Regression
**Random Forest** is an ensemble method that builds multiple decision trees and averages their predictions. It reduces overfitting and improves generalization.

```
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
```

**Pros:**
- Robust and accurate
- Works well with large datasets

**Cons:**
- Less interpretable
- Can be slower for very large datasets

## 5️⃣ Gradient Boosting Machines (e.g., XGBoost, LightGBM)
### Type: Classification and Regression
**Gradient boosting** builds trees sequentially, with each tree learning to fix the errors of the previous ones. Libraries like XGBoost, LightGBM, and CatBoost have become industry standards for predictive modeling competitions and business use cases.

```
import xgboost as xgb
model = xgb.XGBClassifier()
model.fit(X_train, y_train)
```

**Pros:**
- High performance
- Handles missing data and feature importance well

**Cons:**
- Requires tuning
- Longer training times compared to simpler models

## 6️⃣ Support Vector Machines (SVM)
### Type: Classification and Regression
**SVMs** find the optimal hyperplane that separates classes in high-dimensional space. They can use different kernels to model non-linear decision boundaries.

```
from sklearn.svm import SVC
model = SVC(kernel='rbf')
model.fit(X_train, y_train)
```

**Pros:**
- Effective in high-dimensional spaces
- Memory efficient

**Cons:**
- Not ideal for large datasets
- Less interpretable

## 7️⃣ K-Nearest Neighbors (KNN)
### Type: Classification and Regression
**KNN** makes predictions based on the majority label (for classification) or average value (for regression) of the nearest k neighbors.

```
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

**Pros:**
- Simple and intuitive
- No training time

**Cons:**
- Slow for large datasets
- Sensitive to feature scaling and noisy data

## 8️⃣ Artificial Neural Networks (ANN)
### Type: Classification and Regression
**ANNs** are inspired by biological neurons and can model complex, non-linear relationships. They are the foundation of deep learning.

```
from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(64, activation='relu', input_dim=10))
model.add(Dense(1, activation='sigmoid'))
model.fit(X_train, y_train)
```

**Pros:**
- Powerful for non-linear problems
- Scalable to large datasets

**Cons:**
- Requires tuning and compute power
- Less interpretable

## 9️⃣ Naive Bayes
### Type: Classification
A probabilistic classifier based on **Bayes’ Theorem**. Commonly used in text classification (e.g., spam detection).

```
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
```  

**Pros:**  
- Fast and efficient  
- Performs well on text data  

**Cons:**  
- Assumes feature independence  
- Not ideal for complex feature relationships  
