# Prediction types

## Classification  
Classification is the task of predicting a categorical outcome. This means that the model assigns an input to one of several predefined classes or categories.

Examples of Classification Problems:
Email spam detection: Predicting whether an email is “spam” or “not spam.”
Medical diagnosis: Determining whether a tumor is “malignant” or “benign.”
Customer churn: Predicting if a customer will “stay” or “leave.”
Sentiment analysis: Classifying a text as “positive,” “neutral,” or “negative.”
Classification tasks can be further divided into:

Binary classification: Two possible outcomes (e.g., yes/no, true/false)
Multi-class classification: More than two distinct classes (e.g., classifying animal images as cats, dogs, or birds)
Multi-label classification: Multiple labels can be assigned to a single observation (e.g., tagging an article with multiple topics)
Classification algorithms include Logistic Regression, Decision Trees, Random Forests, Support Vector Machines, and Neural Networks, among others.

## Regression
Regression is the task of predicting a continuous numerical value. The model learns the relationship between input features and a target numeric variable.

### Examples of Regression Problems:
- House price prediction: Estimating the selling price of a home based on size, location, and other features.  
- Stock price forecasting: Predicting the future value of a company’s stock.  
- Weather prediction: Estimating temperature, humidity, or rainfall levels.  
- Sales forecasting: Predicting future product sales based on historical data.

Common regression algorithms include Linear Regression, Decision Trees, Random Forest Regressors, Support Vector Regressors, Gradient Boosting Regressors, and Neural Networks.

### Key Considerations When Defining Prediction Problems:
- Output type: Is the prediction a category or a number?  
- Evaluation metrics: Classification uses metrics like accuracy and F1-score, while regression uses metrics like MAE and RMSE.  
- Data distribution: Class imbalance or outliers may affect model choice and training strategy.  
- Business context: Different prediction types align with different business goals—understanding the use case helps select the correct model type.  

In practice, framing the prediction problem accurately helps in choosing the appropriate preprocessing techniques, model algorithms, and performance evaluation criteria. This ultimately leads to better predictive accuracy and more actionable insights.



