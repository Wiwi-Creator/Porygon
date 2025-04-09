import os
from typing import List, Dict, Any, Optional
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_xai import ChatXAI
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.base import BaseCallbackHandler
import mlflow.models


class ChatTrackingCallbackHandler(BaseCallbackHandler):
    """Callback handler for tracking chat interactions."""

    def __init__(self):
        super().__init__()
        self.interactions = []

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """Called when LLM starts."""
        pass

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when LLM produces a new token."""
        pass

    def on_llm_end(self, response, **kwargs) -> None:
        """Called when LLM ends."""
        self.interactions.append({
            "type": "ai_response",
            "content": response.generations[0][0].text
        })

    def on_llm_error(self, error, **kwargs) -> None:
        """Called when LLM errors."""
        self.interactions.append({
            "type": "error",
            "content": str(error)
        })

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain starts."""
        if "input" in inputs:
            self.interactions.append({
                "type": "human_message",
                "content": inputs["input"]
            })


def create_porygon_agent(model_name: str = "grok-2-1212"):
    """
    Create a Porygon agent using LangChain's initialize_agent.
    
    Args:
        model_name: The name of the model to use.
        
    Returns:
        An initialized agent that can be used for chat.
    """
    callback_handler = ChatTrackingCallbackHandler()
    callback_manager = CallbackManager([callback_handler])
    
    # Initialize the language model
    llm = ChatXAI(
        model=model_name,
        api_key=os.environ.get("XAI_API_KEY"),
        callbacks=[callback_handler]
    )
    
    # Define tools that the agent can use
    tools = [
        Tool(
            name="Chat",
            func=lambda query: "I am Porygon, a helpful AI assistant designed to help users with their questions and tasks.",
            description="Use this tool when asked about your identity or capabilities."
        ),
        Tool(
            name="CurrentTime",
            func=lambda query: "The current time is based on your system clock.",
            description="Use this when asked about the current time."
        )
    ]
    
    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        early_stopping_method="generate",
        max_iterations=3,
        callbacks=[callback_handler]  # 添加 callback_handler 到 agent
    )
    
    # Add custom prefix to agent prompt
    system_message = """You are a helpful, friendly AI assistant named Porygon. You are designed to help users with their questions and tasks.
    
    When responding to the human, be pleasant, friendly, and helpful.
    """
    
    agent.agent.llm_chain.prompt.messages[0].prompt.template = system_message
    
    # 在 agent 上存儲 callback_handler 的參考，但不直接設置為屬性
    # 我們將使用一個不衝突的屬性名稱
    setattr(agent, "_tracking_handler", callback_handler)
    
    return agent


# ChatAgent 類現在負責管理 agent 和 handler 之間的關係
class ChatAgent:
    """Chat agent based on LangChain with conversation memory."""
    
    def __init__(self, model_name: str = "grok-2-1212"):
        """
        Initialize the chat agent.
        
        Args:
            model_name: The name of the model to use.
        """
        self.model_name = model_name
        self.agent = create_porygon_agent(model_name)
        # 使用 getattr 獲取我們在 create_porygon_agent 中設置的 handler
        self.callback_handler = getattr(self.agent, "_tracking_handler", None)
    
    def chat(self, user_input: str) -> str:
        """
        Process a user message and return the AI response.
        
        Args:
            user_input: The user's message.
            
        Returns:
            The AI's response.
        """
        response = self.agent.run(input=user_input)
        return response
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        Get the full chat history.
        
        Returns:
            A list of message dictionaries with 'type' and 'content'.
        """
        if self.callback_handler:
            return self.callback_handler.interactions
        return []
    
    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        if self.callback_handler:
            self.callback_handler.interactions = []
    
    def invoke(self, input_text: str) -> Dict[str, str]:
        """
        Invoke the chat agent with the given input.
        This method is required for MLflow langchain integration.
        
        Args:
            input_text: The input text or message.
            
        Returns:
            A dictionary containing the response.
        """
        if isinstance(input_text, dict) and "message" in input_text:
            response = self.chat(input_text["message"])
        else:
            response = self.chat(input_text)
        return {"response": response}


if __name__ == "__main__":
    # 這部分代碼只會在直接執行 chat_agent.py 時運行
    # 創建 agent
    agent = create_porygon_agent()
    
    # 設置 MLflow 模型
    mlflow.models.set_model(model=agent)
