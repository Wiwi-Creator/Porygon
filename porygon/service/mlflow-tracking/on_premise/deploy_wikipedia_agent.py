import os
import mlflow
from mlflow.models import infer_signature
from wikipedia_agent import agent


mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_registry_uri("http://localhost:5000")
mlflow.langchain.autolog()

EXPERIMENT_NAME = "Porygon_EXPERIMENT"
AGENT_NAME = "Porygon_wikipedia_agent"

experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)

mlflow.langchain.autolog()

input_example = {"input": "Who is the highest Pokemon?"}
output_example = agent.invoke(input_example)
signature = infer_signature(input_example, output_example)
tags = {'Knowledge': 'Pokemon', 'Type': 'Wikipedia', 'Model': 'Grok-2-1212'}

with mlflow.start_run(run_name="porygon-wikipedia-agent", tags=tags) as run:
    try:
        model_info = mlflow.langchain.log_model(
            lc_model=os.path.join(os.getcwd(), 'wikipedia_agent.py'),
            artifact_path="porygon_chain",
            input_example=input_example,
            signature=signature
        )

        print(f"Model uri: {model_info.model_uri}")
        registered_model = mlflow.register_model(
            model_uri=model_info.model_uri,
            name=AGENT_NAME
        )
        print(f"Registered model: {registered_model.name} version {registered_model.version}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
