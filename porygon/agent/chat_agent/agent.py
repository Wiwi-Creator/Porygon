import os
import mlflow
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_xai import ChatXAI


def search_tool(query: str) -> str:
    """Simulate a search tool"""
    return f"This is the search result for '{query}'."


def calculator_tool(query: str) -> str:
    """Simple calculator tool"""
    return str(eval(query))


tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="Use this when you need to search for information. Input should be a search query."
    ),
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Use this to perform mathematical calculations. Input should be a mathematical expression."
    )
]

#llm = AzureChatOpenAI(
#    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
#    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
#    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
#    temperature=0.1
#)

llm = ChatXAI(
        model="grok-2-1212",
        api_key=os.environ["XAI_API_KEY"]
        )

tool_descriptions = render_text_description(tools)
tool_names = ", ".join([tool.name for tool in tools])

prompt = PromptTemplate.from_template("""
                                    You are a helpful assistant.
                                    You can use the following tools to answer user questions:
                                    {tools}

                                    Use the following format:
                                    Question: The user's question
                                    Thought: How you should solve this problem
                                    Action: one of [{tool_names}]
                                    Action Input: The input to the tool
                                    Observation: The result from the tool
                                    ... (You can repeat Action/Action Input/Observation steps)
                                    Thought: Now I know the final answer
                                    Final Answer: The final answer to give to the user

                                    Question: {input}
                                    {agent_scratchpad}
                                    """)

# Create AI Agent
agent = create_react_agent(
    llm,
    tools,
    prompt.partial(
        tools=tool_descriptions,
        tool_names=tool_names
    )
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

mlflow.models.set_model(agent_executor)
