import os
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage


def search_tool(query: str) -> str:
    """Simulate a search tool"""
    return f"This is the search result for '{query}'."


def calculator_tool(query: str) -> str:
    """Simple calculator tool"""
    try:
        return str(eval(query))
    except:
        return "Calculation error, please check the input format"


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


llm = AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            temperature=0.1
            )

prompt = ChatPromptTemplate.from_messages([
            SystemMessage(
                content="""You are a helpful assistant.
                            You can use the following tools to answer user questions:
                            Search: Use this to search for information
                            Calculator: Use this to perform mathematical calculations

                            Use the following format:
                            Question: The user's question
                            Thought: How you should solve this problem
                            Action: The tool name
                            Action Input: The input to the tool
                            Observation: The result from the tool
                            ... (You can repeat Action/Action Input/Observation steps)
                            Thought: Now I know the final answer
                            Final Answer: The final answer to give to the user
                        """),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
                    ]
                                          )

# Create AI Agent
agent = create_react_agent(llm, tools, prompt)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Test Agent via API (FastAPI)
response = agent_executor.invoke({"input": "What is artificial intelligence? Then calculate 2+2 equals what?"})
print(response["output"])
