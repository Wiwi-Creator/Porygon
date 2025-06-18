import dspy
import mlflow
from agent import DSPyAirlineCustomerService


mlflow.set_registry_uri("https://mlflow-931091704211.asia-east1.run.app")
mlflow.set_tracking_uri("https://mlflow-931091704211.asia-east1.run.app")

EXPERIMENT_NAME = "DSPy_Agent_Deploy"
experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    print(f"Experiment {EXPERIMENT_NAME} not found, creating a new one...")
    mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(EXPERIMENT_NAME)

tools = await session.list_tools()
mlflow.dspy.autolog(log_traces_from_eval)
dspy_tools = []
for tool in tools.tools:
    dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))
react = dspy.ReAct(DSPyAirlineCustomerService, tools=dspy_tools)

with mlflow.start_run():
    model_info = mlflow.dspy.log_model(
        DSPyAirlineCustomerService,
        artifact_path="model",
        input_example="Book a Flight for me.",
    )
