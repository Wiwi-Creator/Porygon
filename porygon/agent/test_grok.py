import os
from langchain_xai import ChatXAI
from langchain_core.messages import HumanMessage


llm = ChatXAI(
    model="grok-2-1212",
    api_key=os.environ["XAI_API_KEY"])

response = llm.invoke([HumanMessage(content='Hey how are you?')])
print(response)
