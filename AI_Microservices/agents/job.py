# agents/wikipedia_agent/job.py
import os
import json
import argparse
import mlflow.pyfunc
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wikipedia_agent")

def run_wikipedia_agent(query: str, output_path: str) -> None:
    """運行 Wikipedia Agent 並將結果儲存到指定路徑"""
    try:
        logger.info(f"Loading model for query: {query}")
        
        # 從 MLflow 加載模型
        model_uri = os.environ.get("MODEL_URI", "models:/wikipedia-agent/production")
        model = mlflow.pyfunc.load_model(model_uri)
        
        # 準備輸入並進行預測
        model_input = [{"input": query}]
        logger.info(f"Running prediction with input: {model_input}")
        prediction = model.predict(model_input)
        
        # 格式化預測結果
        if isinstance(prediction, list) and len(prediction) > 0:
            answer = str(prediction[0])
        else:
            answer = str(prediction)
            
        result = {
            "responseCode": 200,
            "responseMessage": "OK",
            "results": [{"answers": answer}]
        }
        
        # 將結果寫入輸出文件
        with open(output_path, 'w') as f:
            json.dump(result, f)
            
        logger.info(f"Results saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Error running Wikipedia Agent: {str(e)}")
        
        # 將錯誤寫入輸出文件
        error_result = {
            "responseCode": 500,
            "responseMessage": f"Error: {str(e)}",
            "results": []
        }
        
        with open(output_path, 'w') as f:
            json.dump(error_result, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wikipedia Agent Job")
    parser.add_argument("--query", type=str, required=True, help="User query")
    parser.add_argument("--output", type=str, required=True, help="Output file path")
    args = parser.parse_args()
    
    run_wikipedia_agent(args.query, args.output)