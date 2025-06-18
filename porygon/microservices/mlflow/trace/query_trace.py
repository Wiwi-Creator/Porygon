import mlflow


mlflow.set_registry_uri("https://mlflow-931091704211.asia-east1.run.app")
mlflow.set_tracking_uri("https://mlflow-931091704211.asia-east1.run.app")

traces = mlflow.search_traces(experiment_ids=["14"], run_id="bff3a5dfe1414d16af640ad25186ad67")
print(traces)
traces.to_csv('traces_debug.csv')
