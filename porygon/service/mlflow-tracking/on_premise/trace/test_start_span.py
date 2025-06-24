import uuid
import mlflow
from mlflow.entities import SpanType
from langchain_xai import ChatXAI

llm = ChatXAI(model="grok-2-1212")

mlflow.set_registry_uri("https://mlflow-931091704211.asia-east1.run.app")
mlflow.set_tracking_uri("https://mlflow-931091704211.asia-east1.run.app")
EXPERIMENT_NAME = "Test_Chat_bot"
experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(EXPERIMENT_NAME)

#mlflow.langchain.autolog()


def start_session():
    with mlflow.start_run(run_name="Chat_Bot_Session_v2"):
        while True:
            user_input = input("You: ")
            if user_input.upper() == "BYE":
                break

            request_id = str(uuid.uuid4())

            with mlflow.start_span(
                name="UserInteraction",
                span_type=SpanType.AGENT,
                attributes={"request_id": request_id}
            ) as span:
                span.set_inputs(user_input)

                result = llm.invoke([
                    {"role": "system", "content": "You are a friendly chat bot"},
                    {"role": "user", "content": user_input}
                ])
                answer = result.content

                span.set_outputs(answer)

            print(f"Bot: {answer}")


start_session()
