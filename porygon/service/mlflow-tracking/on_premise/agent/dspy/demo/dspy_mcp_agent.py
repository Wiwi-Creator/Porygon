from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import dspy
import mlflow
from mlflow.entities import SpanType
import time
import tiktoken

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

class SimpleBaseline(dspy.Signature):
    """Simple airline customer service response without tools"""
    user_request: str = dspy.InputField()
    response: str = dspy.OutputField()

def count_tokens(text: str) -> int:
    """Simple token counting function"""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except:
        # Fallback: rough estimate
        return len(text.split()) * 1.3

dspy.configure(lm=dspy.LM("xai/grok-2-1212"))

async def run(user_request):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()
            
            # MLflow setup
            mlflow.dspy.autolog()
            mlflow.set_tracking_uri("http://localhost:5000")
            mlflow.set_registry_uri("http://localhost:5000")

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
            
            with mlflow.start_run(run_name="MCP_Agent_Run_Enhanced"):
                # Basic parameters
                mlflow.log_param("request", user_request)
                mlflow.log_param("request_length", len(user_request))
                mlflow.log_param("available_tools", len(dspy_tools))

                # Count input tokens
                input_tokens = count_tokens(user_request)
                mlflow.log_metric("input_tokens", input_tokens)

                # Get baseline response (without tools)
                print("Getting baseline response...")
                baseline_start = time.time()
                baseline_agent = dspy.Predict(SimpleBaseline)
                baseline_result = baseline_agent(user_request=user_request)
                baseline_latency = time.time() - baseline_start
                baseline_tokens = count_tokens(baseline_result.response)

                # Log baseline metrics
                mlflow.log_metric("baseline_tokens", baseline_tokens)
                mlflow.log_metric("baseline_latency", baseline_latency)
                mlflow.log_text(baseline_result.response, "baseline_response.txt")

                # Run agent with tools
                print("Running agent with tools...")
                agent_start = time.time()
                react = dspy.ReAct(DSPyAirlineCustomerService, tools=dspy_tools)
                result = await react.acall(user_request=user_request)
                agent_latency = time.time() - agent_start

                # Count output tokens
                output_tokens = count_tokens(result.process_result)
                total_tokens = input_tokens + output_tokens

                # Log agent metrics
                mlflow.log_metric("output_tokens", output_tokens)
                mlflow.log_metric("total_tokens", total_tokens)
                mlflow.log_metric("agent_latency", agent_latency)

                # Calculate comparisons
                token_efficiency = baseline_tokens / output_tokens if output_tokens > 0 else 1.0
                latency_ratio = baseline_latency / agent_latency if agent_latency > 0 else 1.0

                mlflow.log_metric("token_efficiency", token_efficiency)
                mlflow.log_metric("latency_ratio", latency_ratio)

                mlflow.log_text(result.process_result, "agent_response.txt")

if __name__ == "__main__":
    import asyncio

    asyncio.run(run("please help me book a flight from SFO to JFK on 09/01/2025, my name is Wiwi"))
