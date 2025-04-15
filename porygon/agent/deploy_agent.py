# deploy_agent.py
import os
import sys
import mlflow

# 設置MLflow參數
mlflow.set_tracking_uri("http://localhost:5010")
mlflow.set_registry_uri("http://localhost:5010")

EXPERIMENT_NAME = "/Users/w22151500@gmail.com/Porygon_Agent_V4"
AGENT_NAME = "Porygon_wikipedia_agent"

# 檢查或創建實驗
experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment_info:
    mlflow.set_experiment(experiment_id=experiment_info.experiment_id)
else:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_id=experiment_id)

# 創建範例輸入
input_example = {"input": "Who is the highest Pokemon?"}

# 獲取當前目錄和模型文件路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
model_file = os.path.join(current_dir, "agent_model.py")

print(f"當前目錄: {current_dir}")
print(f"模型文件路徑: {model_file}")
print(f"文件是否存在: {os.path.exists(model_file)}")

# 確保模型文件在Python路徑中
sys.path.append(current_dir)

# 記錄標籤
tags = {'Knowledge': 'Pokemon', 'Type': 'Wikipedia', 'Model': 'Grok-2-1212'}

with mlflow.start_run(run_name="porygon-wikipedia-agent", tags=tags) as run:
    try:
        # 直接創建一個實例作為備選方案
        from agent_model import PorygonAgent
        model_instance = PorygonAgent()
        
        # 使用實例方法
        model_info = mlflow.pyfunc.log_model(
            artifact_path="porygon_chain",
            python_model=model_instance,
            code_path=[model_file],  # 使用實際文件路徑
            input_example=input_example,
            pip_requirements=[
                "langchain>=0.3.0",
                "langchain-community>=0.3.0", 
                "langchain-xai>=0.2.0",
                "wikipedia>=1.4.0"
            ]
        )
        
        print(f"Model uri: {model_info.model_uri}")
        
        # 註冊模型
        registered_model = mlflow.register_model(
            model_uri=model_info.model_uri,
            name=AGENT_NAME
        )
        print(f"Registered model: {registered_model.name} version {registered_model.version}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()