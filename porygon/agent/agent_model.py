# agent_model.py
import mlflow.pyfunc
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_xai import ChatXAI


class PorygonAgent(mlflow.pyfunc.PythonModel):
    def __init__(self):
        # 空的初始化函數，避免序列化問題
        pass
        
    def load_context(self, context):
        # 加載模型時初始化所有組件
        self.llm = ChatXAI(model="grok-2-1212")
        self.tools = load_tools(["wikipedia"], llm=self.llm)
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=False
        )
    
    def predict(self, context, model_input):
        """處理查詢請求"""
        try:
            if isinstance(model_input, dict):
                query = model_input.get("input", "")
                if not query:
                    return {"error": "No input provided"}
                
                result = self.agent.invoke({"input": query})
                return result
                
            elif isinstance(model_input, list):
                results = []
                for item in model_input:
                    query = item.get("input", "")
                    if query:
                        result = self.agent.invoke({"input": query})
                        results.append(result)
                    else:
                        results.append({"error": "No input provided"})
                return results
            else:
                return {"error": "Unsupported input format"}
        except Exception as e:
            return {"error": str(e)}