import os
import mlflow
from mlflow.pyfunc import PythonModel
from mlflow.models.signature import infer_signature
import datetime
from agent.agent import agent_executor


mlflow.set_tracking_uri("http://localhost:5000")
mlflow.langchain.autolog()
UC_MODEL_NAME = "Porygon_agent"
EXPERIMENT_NAME = "/Users/w22151500@gmail.com/Porygon_demo"


class AgentWrapper(PythonModel):
    def __init__(self, agent):
        self.agent = agent

    def predict(self, context, model_input):
        if isinstance(model_input, dict):
            query = model_input.get("input", "")
        else:
            query = model_input
        result = self.agent.invoke({"input": query})
        return result


experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)

input_example = {"input": "What is the capital of France?"}
output_example = {"output": "The capital of France is Paris."}
signature = infer_signature(input_example, output_example)
agent_model = AgentWrapper(agent_executor)

with mlflow.start_run(run_name=f"Demo_Agent_deploy-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}"):
    logged_agent_info = mlflow.pyfunc.log_model(
        python_model=os.path.join(os.getcwd(), 'agent.py'),
        artifact_path='AI_Agent',
        signature=signature,
        input_example=input_example
    )

uc_registered_model_info = mlflow.register_model(
    model_uri=logged_agent_info.model_uri,
    name=UC_MODEL_NAME
)
