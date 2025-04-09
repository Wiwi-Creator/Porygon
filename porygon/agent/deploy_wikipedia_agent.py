import mlflow
from mlflow.models import infer_signature
from chat_agent.wikipedia_agent import agent

mlflow.set_tracking_uri("http://localhost:5010")
mlflow.set_registry_uri("http://localhost:5500")
EXPERIMENT_NAME = "/Users/w22151500@gmail.com/Porygon_demo"
AGENT_NAME = "Porygon_wikipedia_agent"

experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)

mlflow.langchain.autolog()

input_example = {"input": "Who is the highest Pokemon?"}
tags = {'Knowledge': 'Pokemon', 'Type': 'Wikipedia', 'Model': 'Grok-2-1212'}
with mlflow.start_run(run_name="porygon-wikipedia-agent", tags=tags) as run:
    try:
        # invoke
        prediction = agent.invoke(input_example)
        # model registry
        model_info = mlflow.langchain.log_model(
            lc_model=agent,
            artifact_path="porygon-chain",
            input_example=input_example,
            signature=infer_signature(input_example, prediction),
        )

        print(f"Model uri: {model_info.model_uri}")
    except Exception as e:
        print(f"Error : {e}")

mlflow.register_model(
        model_uri=model_info.model_uri,
        name=AGENT_NAME
)
