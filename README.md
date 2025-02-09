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


## EDA

The folder analysis `analysis/analyze_src` contains all the necessary functions for EDA following strategy and template design pattenrs. `analysis/EDA.ipynb` is a python notebook where all the EDA is done and the right analysis is performed.

## Training Pipeline with ZenML

In this training_pipeline.py file, it is defined an end-to-end machine learning pipeline for predicting house prices using ZenML. The pipeline consists of multiple steps, starting with data ingestion from a compressed archive, followed by handling missing values, feature engineering, and outlier detection. After data preprocessing, the pipeline splits the dataset into training and testing sets, builds a predictive model, and evaluates its performance using key metrics like mean squared error (MSE). The pipeline is structured using modular ZenML steps, ensuring flexibility and reusability.

This setup automates the entire machine learning workflow, making it easier to train, test, and deploy models in a structured way. The use of ZenML provides a robust framework for managing ML experiments, enabling efficient tracking of data transformations, model performance, and versioning. By executing ml_pipeline(), the script runs all these steps sequentially, producing a trained model that can later be used for predictions in a production environment.

If you are running the run_deployment.py script, you will also need to install some integrations using ZenML:

```
zenml integration install mlflow -y 
```

The project can only be executed with a ZenML stack that has an MLflow experiment tracker and model deployer as a component. Configuring a new stack with the two components are as follows:

```
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml model-deployer register mlflow --flavor=mlflow
zenml stack register local-mlflow-stack -a default -o default -d mlflow -e mlflow_tracker --set
```

You can run the following command to create an account and have access to the interface.
(Just follow the 1 minute tutorial of zenml)

```
zenml login --local
```




# Re use Code below/comments


