import mlflow


MLFLOW_URI = "http://localhost:5010"

mlflow.set_registry_uri(MLFLOW_URI)
mlflow.set_tracking_uri(MLFLOW_URI)

traces = mlflow.search_traces(experiment_ids=["14"], run_id="bff3a5dfe1414d16af640ad25186ad67")
print(traces)
traces.to_csv('traces_debug.csv')
