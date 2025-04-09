import os
from typing import List, Dict, Any
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_xai import ChatXAI
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.base import BaseCallbackHandler


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


class ChatAgent:
    """Chat agent based on LangChain with conversation memory."""

    def __init__(self, model_name: str = "grok-2-1212"):
        """
        Initialize the chat agent.

        Args:
            model_name: The name of the model to use.
        """
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

    def chat(self, user_input: str) -> str:
        """
        Process a user message and return the AI response.

        Args:
            user_input: The user's message.

        Returns:
            The AI's response.
        """
        response = self.conversation.predict(input=user_input)
        return response

    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        Get the full chat history.

        Returns:
            A list of message dictionaries with 'type' and 'content'.
        """
        # Get interactions from the callback handler
        return self.callback_handler.interactions

    def get_memory_buffer(self) -> str:
        """
        Get the current memory buffer as a string.

        Returns:
            String representation of the memory buffer.
        """
        return self.memory.buffer

    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
        self.callback_handler.interactions = []


# Example usage
if __name__ == "__main__":
    # Set environment variable (for testing)
    if "XAI_API_KEY" not in os.environ:
        os.environ["XAI_API_KEY"] = "your-api-key-here"

    agent = ChatAgent()

    # Example conversation
    response1 = agent.chat("Hello, who are you?")
    print(f"AI: {response1}")

    response2 = agent.chat("What can you help me with?")
    print(f"AI: {response2}")

    # Print chat history
    print("\nChat History:")
    for interaction in agent.get_chat_history():
        print(f"{interaction['type']}: {interaction['content']}")

    # Print memory buffer
    print("\nMemory Buffer:")
    print(agent.get_memory_buffer())
