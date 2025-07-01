"""
Azure ML SDK v2 deployment script for iLearner model
This script uses the modern Azure ML SDK v2 to deploy your model as a managed online endpoint.
"""

from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)
from azure.identity import DefaultAzureCredential
import json

def main():
    # Load workspace configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Create ML Client
    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential=credential,
        subscription_id=config["subscription_id"],
        resource_group_name=config["resource_group"],
        workspace_name=config["workspace_name"]
    )
    
    print(f"Connected to workspace: {config['workspace_name']}")
    
    # Check if model exists, if not register it
    model_name = "ilearner-model-v2"
    try:
        model = ml_client.models.get(name=model_name, version="1")
        print(f"Found existing model: {model.name}, version: {model.version}")
    except:
        print("Registering model with v2 SDK...")
        model = Model(
            path="data.ilearner",
            name=model_name,
            description="iLearner model registered with v2 SDK",
            type="custom_model"
        )
        model = ml_client.models.create_or_update(model)
        print(f"Registered model: {model.name}, version: {model.version}")
    
    # Create environment
    environment_name = "ilearner-env-v2"
    try:
        env = ml_client.environments.get(name=environment_name, version="1")
        print(f"Found existing environment: {env.name}")
    except:
        print("Creating environment...")
        env = Environment(
            name=environment_name,
            description="Environment for iLearner model",
            conda_file="conda_env_v2.yaml",  # Use simpler environment
            image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest"
        )
        env = ml_client.environments.create_or_update(env)
        print(f"Created environment: {env.name}")
    
    # Create endpoint
    from datetime import datetime
    endpoint_name = "ilearner-endpoint"
    
    print(f"Creating endpoint: {endpoint_name}")
    endpoint = ManagedOnlineEndpoint(
        name=endpoint_name,
        description="iLearner model endpoint",
        auth_mode="key"
    )
    
    ml_client.online_endpoints.begin_create_or_update(endpoint).result()
    print(f"Endpoint created: {endpoint_name}")
    
    # Create deployment
    deployment_name = "blue"
    print(f"Creating deployment: {deployment_name}")
    
    deployment = ManagedOnlineDeployment(
        name=deployment_name,
        endpoint_name=endpoint_name,
        model=model,
        environment=env,
        code_configuration=CodeConfiguration(
            code="model/.",
            scoring_script="new_score.py"  # Use the improved scoring script
        ),
        instance_type="Standard_F2s_v2",  # Use smaller instance with only 2 cores
        instance_count=1
    )
    
    ml_client.online_deployments.begin_create_or_update(deployment).result()
    print(f"Deployment created: {deployment_name}")
    
    # Set traffic to 100% for this deployment
    endpoint.traffic = {deployment_name: 100}
    ml_client.online_endpoints.begin_create_or_update(endpoint).result()
    
    # Get the scoring URI
    endpoint = ml_client.online_endpoints.get(name=endpoint_name)
    print(f"\\n✅ Deployment successful!")
    print(f"Endpoint name: {endpoint_name}")
    print(f"Scoring URI: {endpoint.scoring_uri}")
    print(f"Auth mode: {endpoint.auth_mode}")
    
    # Get the auth key
    keys = ml_client.online_endpoints.get_keys(name=endpoint_name)
    print(f"Primary key: {keys.primary_key}")
    
    return endpoint_name, endpoint.scoring_uri, keys.primary_key

if __name__ == "__main__":
    try:
        endpoint_name, scoring_uri, auth_key = main()
        
        # Save deployment info for testing
        deployment_info = {
            "endpoint_name": endpoint_name,
            "scoring_uri": scoring_uri,
            "auth_key": auth_key
        }
        
        with open("deployment_info.json", "w") as f:
            json.dump(deployment_info, f, indent=2)
        
        print(f"\\nDeployment info saved to deployment_info.json")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        raise
