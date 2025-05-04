from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.prompts import PromptTemplate
from langchain_xai import ChatXAI
from langfuse.callback import CallbackHandler

# 載入環境變數
load_dotenv()

# 方法 1: 讓 CallbackHandler 自動從環境變數讀取設定
callback_handler = CallbackHandler()

# 或方法 2: 明確指定配置參數
callback_handler = CallbackHandler(
    secret_key="sk-lf-ec2dbebe-9c2e-41d2-a593-313f0ffac570",
    public_key="pk-lf-4abbf2ba-a2a5-488c-8f70-d80d6a763109",
    host="http://localhost:3000"
)

# 如果您需要 Langfuse 實例進行其他操作，可以單獨創建
# langfuse = Langfuse(
#     secret_key="sk-lf-ec2dbebe-9c2e-41d2-a593-313f0ffac570",
#     public_key="pk-lf-4abbf2ba-a2a5-488c-8f70-d80d6a763109",
#     host="http://localhost:3000"
# )

llm = ChatXAI(
    model="grok-2-1212",
    callbacks=[callback_handler]
)

prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are a helpful assistant named Porygon. You are designed to help users with their questions and tasks. Please answer the following question thoroughly and accurately:

    Question: {question}

    Answer:
    """
)

tools = load_tools(["wikipedia"], llm=llm)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    max_iterations=3,
    early_stopping_method="generate",
    callbacks=[callback_handler]
)

# 測試 agent
response = agent.run("What is the capital of France?")
print(response)
