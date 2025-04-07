import mlflow
import datetime
from databricks import agents
from databricks.sdk import WorkspaceClient
import os


mlflow.set_tracking_uri("http://localhost:5500")
mlflow.set_registry_uri("http://localhost:5000")
mlflow.langchain.autolog()
mlflow.login()


MODEL_NAME = "bugzilla_rag_agent"
w = WorkspaceClient()

experiment_info = mlflow.get_experiment_by_name("/Users/wiwi_kuo@compal.com/Bugzilla_chatbot_demo")
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment("/Users/wiwi_kuo@compal.com/Bugzilla_chatbot_demo")
    mlflow.set_experiment(experiment_id=experiment_id)

with mlflow.start_run(run_name=f"Chat_agent_deploy-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}"):
    logged_agent_info = mlflow.pyfunc.log_model(
        python_model=os.path.join(os.getcwd(), 'chat_chain.py'),
        artifact_path='chat_chain',
    )

uc_registered_model_info = mlflow.register_model(model_uri=logged_agent_info.model_uri, name=MODEL_NAME)
