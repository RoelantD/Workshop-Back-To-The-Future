# Train a machine learning model using designer

This section explains how to use the Azure Machine Learning designer to train a multi-class classification model that predicts results of football matches. 

To learn more about the designer, check out the [Microsoft docs](https://learn.microsoft.com/en-us/azure/machine-learning/concept-designer).

    ⚠️ Please note we are using the classic prebuilt components in this workshop. These will be
    TODO

## Create a new pipeline
Azure Machine Learning pipelines organize multiple machine learning and data processing steps into a single resource. Pipelines let you organize, manage, and reuse complex machine learning workflows across projects and users.

To create an Azure Machine Learning pipeline, you need an Azure Machine Learning workspace. In this section, you learn how to create both these resources.

### Verify you have workspace
You need an Azure Machine Learning workspace to use the designer. The workspace is the top-level resource for Azure Machine Learning. It provides a centralized place to work with all the artifacts you create in Azure Machine Learning. If you have not created a workspace [do so now](/part-1/1-create-ml-workspace.md).

### Create the pipeline

1. Sign in to the Azure Machine Learning studio, and select the workspace you want to use.

1. Select **Designer** from the sidebar menu. Under **Classic prebuilt**, choose **Create a new pipeline using classic prebuilt components**.

1. Select the pencil icon next to the automatically generated pipeline draft name, rename it to **Football result prediction**. The name doesn't need to be unique.

### Import data

There are several sample datasets included in the designer for you to experiment with. For this section use **football-result.csv**

TODO import dataset

1. To the left of the pipeline canvas is a palette of datasets, models and components. Select **Data**.

2. Select the dataset **football-results**, and drag it onto the canvas.


### Visualize the data
You can visualize the data to understand the dataset that you'll use.

1. Right-click the football-results and select **Preview Data**.  

1. Select the different columns in the data window to view information about each one.  

1. Each row represents a result of a football match, and the variables associated with each match appear as columns. There are 13872 rows, 1 header and 15 columns in this dataset.


### Prepare data
Datasets typically require some preprocessing before analysis. You might have noticed some missing values when you inspected the dataset. These missing values must be cleaned so that the model can analyze the data correctly.

TODO empty values

### Remove a column
When you train a model, you must do something about the data that's missing. In this dataset, the **NumberSpectators** column is missing many values, so you exclude that column from the model altogether.

1. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Select Columns in Dataset** component.

1. Drag the **Select Columns in Dataset** component onto the canvas. Drop the component below the dataset component.

1. Connect the **football-results** dataset to the **Select Columns in Dataset** component. Drag from the dataset's output port, which is the small circle at the bottom of the dataset on the canvas, to the input port of **Select Columns in Dataset**, which is the small circle at the top of the component.

    💡Tip
    You create a flow of data through your pipeline when you connect the output port of one component to an input port of another.

![Connect components](/images/connect-components.jpeg)

4. Select the **Select Columns in Dataset** component.

5. Select the arrow icon under **Pipeline interface** to the right of the canvas to open the component details pane. Alternatively, you can double-click the **Select Columns in Dataset** component to open the details pane.

6. Select **Edit column** to the right of the pane.

7. Expand the **Column names** drop down next to **Include**, and select **All columns**.

8. Select the + to add a new rule.

9. From the drop-down menus, select **Exclude** and **Column names**.

10. Enter *NumberSpectators* in the text box.

11. In the lower right, select **Save** to close the column selector.

![Select columns](/images/select-columns.jpeg)

12. In the **Select Columns in Dataset** component details pane, expand **Node information**.

13. Select the **Comment** text box and enter *Exclude number of spectators*.  
Comments appear on the graph to help you organize your pipeline.

### Clean missing data

Your dataset still has missing values after you remove the NumberSpectators column. You can remove the remaining missing data by using the **Clean Missing Data** component.

    💡Tip
    Cleaning the missing values from input data is a prerequisite for using most of the components in the designer.

1. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Clean Missing Data** component.

2. Drag the **Clean Missing Data** component to the pipeline canvas. Connect it to the **Select Columns in Dataset** component.

3. Select the **Clean Missing Data** component.

4. Select the arrow icon under **Pipeline interface** to the right of the canvas to open the component details pane. Alternatively, you can double-click the **Clean Missing Data** component to open the details pane.

5. Select **Edit column** to the right of the pane.

6. In the **Columns to be cleaned** window that appears, expand the drop-down menu next to **Include**. Select **All columns**.

7. Select **Save**.

8. In the **Clean Missing Data** component details pane, under **Cleaning mode**, select **Remove entire row**.

9. In the **Clean Missing Data** component details pane, expand **Node information**.

10. Select the **Comment** text box and enter *Remove missing value rows*.  
Your pipeline should now look something like this:

![Cleaned rows pipeline state](/images/pipeline-state.jpeg)

## Train a machine learning model
Now that you have the components in place to process the data, you can set up the training components.

Because you want to assign a class to your data, you can use a classification algorithm. For this example, you use a logistic regression model.

### Split the data

Splitting data is a common task in machine learning. You'll split your data into two separate datasets. One dataset trains the model and the other tests how well the model performed.

1. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Split Data** component.

2. Drag the **Split Data** component to the pipeline canvas.

3. Connect the left port of the **Clean Missing Data** component to the **Split Data** component.

4. Select the **Split Data** component.

5. Select the arrow icon under **Pipeline interface** to the right of the canvas to open the component details pane. Alternatively, you can double-click the **Split Data** component to open the details pane.

6. In the **Split Data** details pane, set the **Fraction of rows in the first output dataset** to *0.7*.

This option splits 70 percent of the data to train the model and 30 percent for testing it. The 70 percent dataset is accessible through the left output port. The remaining data is available through the right output port.

7. In the **Split Data** details pane, expand **Node information**.

8. Select the **Comment** text box and enter *Split the dataset into training set (0.7) and test set (0.3)*.

### Train the model

Train the model by giving it a dataset that includes the price. The algorithm constructs a model that explains the relationship between the features and the price as presented by the training data.

1. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Multiclass Logistic Regression** component.

2. Drag the **Multiclass Logistic Regression** component to the pipeline canvas.

3. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Train Model** component.

4. Drag the **Train Model** component to the pipeline canvas.

5. Connect the output of the **Multiclass Logistic Regression** component to the left input of the **Train Model** component.

6. Connect the training data output (left port) of the **Split Data** component to the right input of the **Train Model** component.

![Train model overview](/images/train-model.jpeg)

7. Select the **Train Model** component.

8. Select the arrow icon under **Pipeline settings** to the right of the canvas to open the component details pane. Alternatively, you can double-click the **Train Model** component to open the details pane.

9. elect **Edit column** to the right of the pane.

10. In the **Label column** window that appears, expand the drop-down menu and select **Column names**.

11. In the text box, enter *HomeResult* to specify the value that your model is going to predict.  

```
⚠️ Important

Make sure you enter the column name exactly. Don't capitalize price.
```

Your pipeline should look like this:
![Complete pipeline overview](/images/complete-pipeline.jpeg)

### Add the Score Model component

After you train your model by using 70 percent of the data, you can use it to score the other 30 percent to see how well your model functions.

1. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Score Model** component.

2. Drag the **Score Model** component to the pipeline canvas.

3. Connect the output of the **Train Model** component to the left input port of **Score Model**. Connect the test data output (right port) of the **Split Data** component to the right input port of **Score Model**.

### Add the Evaluate Model component
Use the **Evaluate Model** component to evaluate how well your model scored the test dataset.

1. In the datasets and component palette to the left of the canvas, select **Component** and search for the **Evaluate Model** component.

2. Drag the **Evaluate Model** component to the pipeline canvas.

3. Connect the output of the **Score Model** component to the left input of **Evaluate Model**.

The final pipeline should look something like this:
![Complete pipeline overview incl eval](/images/complete-pipeline-with-eval.jpeg)

### Submit pipeline

1. Select **Configure & Submit** in the top corner to submit the pipeline.

2. After the step-by-step wizard appears, follow the wizard to submit the pipeline job. 

3. Select **Create new** under **Experiment name**

4. Configure the experiment, job display name, job description, etc. Click **Next** button.

5. In **Inputs & Outputs**, you can assign value to the inputs and outputs that are promoted to pipeline level. It's empty in this example because we didn't promote any input or output to pipeline level. Click **Next** button.  

6. In **Runtime settings**, you can configure the default datastore and default compute to the pipeline. It's the default datastore and compute for all components in the pipeline. However, if you set a different compute or datastore for a component explicitly, the system respects the component-level setting. Otherwise, it uses the default. Under **Select compute type**, select **Compute instance**.

7. You can only select running compute instances. If the **Compute instance** has stopped, go to **Manage** > **Compute** in the left menu and start the compute in a new tab (CTRL-click the link). You can then refresh the compute instances by clicking **Refresh compute**.
Select the running compute instance. Click **Next** button.

8. The **Review + Submit** step is the last step to review all settings before submit. The wizard remembers your last configuration if you ever submit the pipeline. Click **Submit**

After submitting the pipeline job, there is a message on the top with a link to the job detail. You can select this link to review the job details.

![Submitted pipeline](/images/pipeline-submitted.jpeg)

### View scored labels

In the job detail page, you can check the pipeline job status, results, and logs.

After the job completes, you can view the results of the pipeline job. First, look at the predictions generated by the regression model.

1. Right-click the **Score Model** component, and select **Preview data** > **Scored dataset** to view its output.

Here you can see the predicted prices and the actual prices from the testing data.

![Scored dataset](/images/scored-dataset.jpeg)

### Evaluate models

Use the **Evaluate Model** to see how well the trained model performed on the test dataset.

Right-click the **Evaluate Model** component and select **Preview data** > **Evaluation results** to view its output.
The following statistics are shown for your model:

- **Mean Absolute Error (MAE)**: The average of absolute errors. An error is the difference between the predicted value and the actual value.  
- **Root Mean Squared Error (RMSE)**: The square root of the average of squared errors of predictions made on the test dataset.  
- **Relative Absolute Error**: The average of absolute errors relative to the absolute difference between actual values and the average of all actual values.  
- **Relative Squared Error**: The average of squared errors relative to the squared difference between the actual values and the average of all actual values.  
- **Coefficient of Determination**: Also known as the R squared value, this statistical metric indicates how well a model fits the data.  

For each of the error statistics, smaller is better. A smaller value indicates that the predictions are closer to the actual values. For the coefficient of determination, the closer its value is to one (1.0), the better the predictions.

