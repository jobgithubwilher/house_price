# House Price Project

Project focuses on building an end-to-end ML pipeline for a house price prediction system.

The pipeline is developed using **ZenML** that helps in managing ML workflows, and **MLflow**, which is used for experimenting tracking and model deployment.

**Statistical Problem:** Predict house prices based on various features of the properties: size, location and condition.

**MLOps & Production Readiness**
- Differentitate our project bz integrating MLOps practices using ZenMl and MLFlow.
- Implement CI/CD pipelines to automate testing, deployment, of the model in production.
- Ensure the model is not only accurate but also maintainable, scalable, and readz for real-world use.

## Prepare local environment

Create a virtual env
(my suggestion is Conda Environment)

```
conda create --name house_price_env python=3.9
```

Activate the conda environment

```
conda activate house_price_env
```

Install dependencies

```
pip install -r requirements.txt
```

Install ZenML - https://docs.zenml.io/getting-started/installation 
```
pip install zenml
```

# Re use Code below/comments

Once virtualenv environment is activated, run following command:


If you are running the run_deployment.py script, you will also need to install some integrations using ZenML:

zenml integration install mlflow -y 

The project can only be executed with a ZenML stack that has an MLflow experiment tracker and model deployer as a component. Configuring a new stack with the two components are as follows:

zenml integration install mlflow -y
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml model-deployer register mlflow --flavor=mlflow
zenml stack register local-mlflow-stack -a default -o default -d mlflow -e mlflow_tracker --set
