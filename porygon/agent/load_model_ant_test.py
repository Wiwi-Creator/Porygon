import mlflow
import datetime
import pandas as pd

mlflow.set_tracking_uri("http://localhost:5010")
mlflow.set_registry_uri("http://localhost:5010")
EXPERIMENT_NAME = "/Users/w22151500@gmail.com/Porygon_demo"

experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)

mlflow.langchain.autolog()

model_uri = "runs:/a30454d17c37413ba0bb77c2f66dd102/porygon_chain"
loaded_model = mlflow.pyfunc.load_model(model_uri)

test_questions = [
    "Who is the highest Pokemon?",
    "What is the strongest Pokemon?",
    "Which Pokemon has the most evolutionary forms?",
    "Who created Pokemon?",
    "When was the first Pokemon game released?"
]


tags = {
    "model_type": "LLM_Chain",
    "purpose": "Pokemon_QA",
    "model": "Grok-2-1212"
}


with mlflow.start_run(run_name=f"pokemon_qa_evaluation-{datetime.datetime.now().date()}", tags=tags) as run:

    mlflow.log_param("model_uri", model_uri)
    mlflow.log_param("num_questions", len(test_questions))

    results = []
    for i, question in enumerate(test_questions):

        answer = loaded_model.predict([{"input": question}])[0]

        mlflow.log_text(f"Question: {question}\nAnswer: {answer}", f"qa_pair_{i+1}.txt")

        results.append({"question": question, "answer": answer})

    results_df = pd.DataFrame(results)
    mlflow.log_table(data=results_df, artifact_file="all_qa_results.json")

    example_question = "Who is the highest Pokemon?"
    example_answer = loaded_model.predict([{"input": example_question}])[0]
    mlflow.log_metric("example_answer_length", len(example_answer))

    print(f"Run ID: {run.info.run_id}")
    print(f"Results recorded to MLflow")
