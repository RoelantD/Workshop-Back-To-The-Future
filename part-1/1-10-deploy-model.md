# Deploy a machine learning model using ~~designer~~

If you have not created a pipeline yet, continue with [Training a machine learning model](/part-1/1-9-train-model.md)

To deploy your pipeline, you must first convert the training pipeline into a real-time inference pipeline. This process removes training components and adds web service inputs and outputs to handle requests.

## Create a real-time inference pipeline

1. Select **Jobs** from the sidebar menu, then open the pipeline job that you created. On the detail page, above the pipeline canvas, select the ellipses ... then choose **Create inference pipeline** > **Real-time inference pipeline**.

Your new pipeline now looks like this:
![Inference pipeline](/images/inference-pipeline.jpeg)

When you selected **Create inference pipeline**, several things happened:
- The trained model is stored as a **Dataset** component in the component palette. You can find it under **My Datasets**.  
- Training components like **Train Model** and **Split Data** are removed.  
- The saved trained model is added back into the pipeline.  
- **Web Service Input** and **Web Service Output** components are added. These components show where user data enters the pipeline and where data is returned.  

```
⚠️Note

By default, the Web Service Input expects the same data schema as the component output data that connects to the same downstream port. In this sample, Web Service Input and Automobile price data (Raw) connect to the same downstream component, so Web Service Input expects the same data schema as Automobile price data (Raw) and target variable column price is included in the schema. However, when you score the data, you won't know the target variable values. In that case, you can remove the target variable column in the inference pipeline using the Select Columns in Dataset component. Make sure that the output of Select Columns in Dataset removing target variable column is connected to the same port as the output of the Web Service Input component.
```

2. Select **Configure & Submit**, and use the same compute target and experiment that you used in part one.
If this is the first job, it might take up to 20 minutes for your pipeline to finish running. The default compute settings have a minimum node size of 0, which means that the designer must allocate resources after being idle. Repeated pipeline jobs take less time since the compute resources are already allocated. Additionally, the designer uses cached results for each component to further improve efficiency.

3. Go to the real-time inference pipeline job detail by selecting **Job detail** in the left pane.

4. Select **Deploy** in the job detail page.

## Deploy the real-time endpoint

Azure Machine Learning Studio has an option to deploy a real-time inference endpoint through the UI. That would be amazing if it actually (still) worked. There seems to be a very resilient bug introduced with the recent changes to Azure AI Foundry authentication.

We are therefore going to deploy our inference endpoint by downloading our trained model and using a Python script.

### Downloading our model files

1. Select **Data** in the **Assets** menu on the left side.

2. Select the asset that starts with **MD-**. This will take you to the asset metadata overview.

3. Use the **Storage URI** to navigate to the correct folder in the storage account. This is the storage account that was created alongside the Azure Machine Learning Studio instance. 

4. Download the entire contents of the **Trained_model** folder to the **model** folder in this repository.

5. Note that we are not using **score.py**, but we are using an updated version **score_new.py** when deploying the model.

6. Update **config.json** with the values of your **Azure Machine Learning Workspace**. You can find all three of these values in the Azure Portal on the **Overview** node of the Workspace resource.

7. Open a terminal at the **root** folder of this repository (so make sure you are **NOT** in the model folder.)

8. Run the **deploy.py** script to deploy the endpoint. ⚠️ This will take a couple of minutes.

The deploy script will provide you with the necessary values to use the created endpoint. The endpoint will listen to **POST** requests on the **Scoring URI** and will check for the key in the **Bearer token**.

Set the **Authorization header** to *Bearer [KEY]* and use the following test body:

```
{
  "data": [
    {
      "HomeFPI": 125.5,
      "AwayFPI": 85.2,
      "HomeOdds": 2.1,
      "AwayOdds": 2.2,
      "NumberSpectators": 50000,
      "Weather": "Clear"
    }
  ]
}
```

🥳 You have now succesfully created an endpoint for your newly trained machine learning classification model.

[⏮️ Previous](/part-1/1-9-train-model.md) 
[⏭️ Next](/part-2/2-1-create-vanilla-agent.md)