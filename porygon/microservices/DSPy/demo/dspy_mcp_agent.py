from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import dspy
import mlflow
from mlflow.entities import SpanType

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["mcp_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


class DSPyAirlineCustomerService(dspy.Signature):
    """You are an airline customer service agent. You are given a list of tools to handle user requests.
    You should decide the right tool to use in order to fulfill users' requests."""

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and the information users need, "
            "e.g., the confirmation_number if it's a flight booking request."
        )
    )


dspy.configure(lm=dspy.LM("xai/grok-2-1212"))


async def run(user_request):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()
            mlflow.dspy.autolog()
            mlflow.set_registry_uri("https://mlflow-server-936256038486.asia-east1.run.app")
            mlflow.set_tracking_uri("https://mlflow-server-936256038486.asia-east1.run.app")
            EXPERIMENT_NAME = "DSPy_Airfloght_Agent_DEMO"
            experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
            if experiment_info:
                mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
            else:
                print(f"Experiment {EXPERIMENT_NAME} not found, creating a new one...")
                mlflow.create_experiment(EXPERIMENT_NAME)
                mlflow.set_experiment(EXPERIMENT_NAME)
            # Convert MCP tools to DSPy tools
            dspy_tools = []
            for tool in tools.tools:
                dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))
            with mlflow.start_run(run_name="MCP_Agent_Run"):
                mlflow.log_param("request", user_request)
                mlflow.log_metric("request_length", len(user_request))
                # Create the agent
                react = dspy.ReAct(DSPyAirlineCustomerService, tools=dspy_tools)
                result = await react.acall(user_request=user_request)
                print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run("please help me book a flight from SFO to JFK on 09/01/2025, my name is Wiwi"))
