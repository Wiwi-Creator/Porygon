# app/main.py
import os
from typing import Dict, Optional, List
import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5010")
MODEL_URI = os.getenv("MODEL_URI", "models:/ChatAgent/latest")

# init fastapi app
app = FastAPI(
    title="Porygon Chat API",
    description="An API for interacting with Porygon, an AI assistant powered by Grok-2-1212",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    response: str


@app.on_event("startup")
async def startup_event():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    try:
        global loaded_model
        loaded_model = mlflow.pyfunc.load_model(MODEL_URI)
        print(f"Successfully loaded model from {MODEL_URI}")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e


@app.get("/health")
async def health_check():
    """Check if the API is up and running."""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Porygon and get a response."""
    try:

        if 'loaded_model' not in globals():
            raise HTTPException(status_code=503, detail="Model not loaded yet")

        model_input = {"input": request.message}
        if request.history:
            model_input["history"] = request.history

        result = loaded_model.predict([model_input])[0]

        if isinstance(result, dict) and "response" in result:
            return ChatResponse(response=result["response"])
        else:
            return ChatResponse(response=str(result))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/history")
async def get_history():
    """Get the chat history if available."""
    try:
        if 'loaded_model' not in globals():
            raise HTTPException(status_code=503, detail="Model not loaded yet")

        if hasattr(loaded_model, 'get_chat_history'):
            history = loaded_model.get_chat_history()
            return {"history": history}
        else:
            return {"message": "This model does not support history retrieval"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")


@app.post("/clear")
async def clear_history():
    """Clear the chat history if available."""
    try:
        if 'loaded_model' not in globals():
            raise HTTPException(status_code=503, detail="Model not loaded yet")

        if hasattr(loaded_model, 'clear_memory'):
            loaded_model.clear_memory()
            return {"status": "success", "message": "Chat history cleared"}
        else:
            return {"status": "warning", "message": "This model does not support history clearing"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
