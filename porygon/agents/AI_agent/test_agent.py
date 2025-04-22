import mlflow


mlflow.set_tracking_uri("http://localhost:5010")
mlflow.set_registry_uri("http://localhost:5010")
EXPERIMENT_NAME = "/Users/w22151500@gmail.com/Porygon_demo"

experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)

mlflow.langchain.autolog()


model_uri = "runs:/8fc2bee0fa4547daaa20e6949f5203f2/porygon_chain"
loaded_model = mlflow.pyfunc.load_model(model_uri)
result = loaded_model.predict([{"input": "Who is the highest Pokemon?"}])

print(result)
