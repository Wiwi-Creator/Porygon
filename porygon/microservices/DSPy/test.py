import mlflow
import dspy


llm = dspy.LM("xai/grok-2-1212")
dspy.configure(lm=llm)


class QAModule(dspy.Signature):
    question = dspy.InputField()
    response = dspy.OutputField()


qa = dspy.Predict(QAModule)

question = "What is the capital of France?"

mlflow.set_registry_uri("https://mlflow-server-936256038486.asia-east1.run.app")
mlflow.set_tracking_uri("https://mlflow-server-936256038486.asia-east1.run.app")

EXPERIMENT_NAME = "DSPy_Trace_DEMO"
experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    print(f"Experiment {EXPERIMENT_NAME} not found, creating a new one...")
    mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run():
    result = qa(question=question)
    mlflow.log_param("question", question)
    mlflow.log_text(result.response, "response.txt")
    mlflow.log_metric("response_length", len(result.response))

print("Response:", result.response)
