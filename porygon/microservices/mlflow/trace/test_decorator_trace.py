import mlflow


mlflow.set_registry_uri("https://mlflow-931091704211.asia-east1.run.app")
mlflow.set_tracking_uri("https://mlflow-931091704211.asia-east1.run.app")


@mlflow.trace(span_type="AGENT", attributes={"key": "value"})
def add_1(x):
    return x + 1


@mlflow.trace(span_type="RETRIEVER", attributes={"key1": "value1"})
def minus_1(x):
    return x - 1


@mlflow.trace(name="Trace Test")
def trace_test(x):
    step1 = add_1(x)
    return minus_1(step1)


EXPERIMENT_NAME = "Test_trace"
experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    print(f"Experiment {EXPERIMENT_NAME} not found, creating a new one...")
    mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(run_name="MCP_Agent_Run"):
    trace_test(100)
