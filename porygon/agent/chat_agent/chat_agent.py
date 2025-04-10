import os
from typing import List, Dict, Any, Optional
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_xai import ChatXAI
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
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


class PorygonChatModel(BaseChatModel):
    """Custom chat model wrapper for MLflow compatibility"""
    
    llm: Any
    conversation: Any
    memory: Any
    callback_handler: Any
    
    def __init__(self, model_name: str = "grok-2-1212"):
        """Initialize the chat model."""
        super().__init__()
        self.callback_handler = ChatTrackingCallbackHandler()
        self.callback_manager = CallbackManager([self.callback_handler])

        # Initialize model
        self.llm = ChatXAI(
            model=model_name,
            api_key=os.environ.get("XAI_API_KEY"),
            callbacks=[self.callback_handler]
        )

        # Initialize memory
        self.memory = ConversationBufferMemory()

        # Initialize conversation template
        template = """
        You are a helpful, friendly AI assistant named Porygon. You are designed to help users with their questions and tasks.

        Current conversation:
        {history}

        Human: {input}
        AI:
        """

        prompt = PromptTemplate(input_variables=["history", "input"], template=template)

        # Initialize conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt,
            verbose=True
        )
    
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        """Generate a response."""
        if messages:
            user_input = messages[-1].content
            response = self.conversation.predict(input=user_input)
            from langchain_core.messages import AIMessage
            return {"generations": [[AIMessage(content=response)]]}
        return {"generations": [[]]}
    
    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "porygon_chat_model"

    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the full chat history."""
        return self.callback_handler.interactions

    def get_memory_buffer(self) -> str:
        """Get the current memory buffer as a string."""
        return self.memory.buffer

    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
        self.callback_handler.interactions = []

    def invoke(self, input_text: str) -> Dict[str, str]:
        """Invoke the chat agent with the given input."""
        if isinstance(input_text, str):
            response = self.conversation.predict(input=input_text)
            return {"response": response}
        elif isinstance(input_text, dict) and "message" in input_text:
            response = self.conversation.predict(input=input_text["message"])
            return {"response": response}
        return {"response": "Invalid input format"}


class ChatAgent(PorygonChatModel):
    """Chat agent based on LangChain with conversation memory."""
    pass


chat_agent_config = {
    "model_name": os.environ.get("MODEL_NAME", "grok-2-1212")
}
agent = ChatAgent(model_name=chat_agent_config["model_name"])
mlflow.models.set_model(model=agent)
