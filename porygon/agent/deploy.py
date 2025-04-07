import mlflow
import datetime
from porygon.agent.agent import agent_executor


mlflow.set_tracking_uri("http://localhost:5010")
mlflow.set_registry_uri("http://localhost:5000")
mlflow.langchain.autolog()
mlflow.login()
UC_MODEL_NAME = "Porygon_agent"

experiment_info = mlflow.get_experiment_by_name("/Users/w22151500@gmail.com/Porygon_demo")
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment("/Users/w22151500@gmail.com/Porygon_demo")
    mlflow.set_experiment(experiment_id=experiment_id)

with mlflow.start_run(run_name=f"Demo_Agent_deploy-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}"):
    logged_agent_info = mlflow.langchain.log_model(
        agent_executor,
        artifact_path='AI_Agent',
        extra_params={
            "tools": [tool.name for tool in agent_executor.tools],
            "description": "Muliti-Agent System"
        }
    )

uc_registered_model_info = mlflow.register_model(
    model_uri=logged_agent_info.model_uri,
    name=UC_MODEL_NAME
)
