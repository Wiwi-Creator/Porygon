import mlflow

mlflow.langchain.autolog()
mlflow.set_tracking_uri("https://mlflow-931091704211.asia-east1.run.app")
mlflow.set_registry_uri("https://mlflow-931091704211.asia-east1.run.app")
MODEL_URI = "runs:/07391c9ffc2b4acab430f9ec61bd62ab/porygon_chain"

EXPERIMENT_NAME = "Pokemon_Model_Interactions"
experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)


with mlflow.start_run(run_name="pokemon_height_query"):
    loaded_model = mlflow.pyfunc.load_model(MODEL_URI)
    mlflow.log_param("question", "Who is the highest Pokemon?")
    result = loaded_model.predict([{"input": "Who is the highest Pokemon?"}])
    mlflow.log_metric("response_length", len(str(result)))
    mlflow.log_text(str(result), "response.txt")
    print(result)
