import os
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import load_tools
from langchain_xai import ChatXAI


llm = ChatXAI(
    model="grok-2-1212",
    api_key=os.environ.get("XAI_API_KEY")
)


prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are a helpful assistant named Porygon. You are designed to help users with their questions and tasks. Please answer the following question thoroughly and accurately:
                Question: {question}
                Answer:
            """
    )
tools = load_tools(["serpapi", "wikipedia"], llm=llm)
# Create the agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
