import mlflow
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.prompts import PromptTemplate
from langchain_xai import ChatXAI


llm = ChatXAI(
    model="grok-2-1212"
)

prompt = PromptTemplate(
    input_variables=["input"],
    template="""You are a helpful assistant named Porygon. You are designed to help users with their questions and tasks. Please answer the following question thoroughly and accurately:
                Question: {question}
                Answer:
            """
    )
tools = load_tools(["wikipedia"], llm=llm)
# serpapi
# Create the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    max_iterations=3,
    early_stopping_method="generate"
)
mlflow.models.set_model(model=agent)
