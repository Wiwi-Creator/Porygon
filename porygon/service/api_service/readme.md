# Porygon API 架構詳解

## Architecture

1. **路由層 (Router Layer)**：處理 HTTP request router 和 參數解析
2. **服務層 (Service Layer)**：實現 業務邏輯和模型交互
3. **模型層 (Model Layer)**：加載和使用 AI 模型進行預測
4. **數據層 (Schema Layer)**：定義數據結構和驗證規則
5. **工具層 (Utils Layer)**：提供通用功能和工具方法

## 1. 路由層 (Router Layer)

位於 `porygon_api/app/agent/router.py` 和 `porygon_api/app/agent/v1/wikipedia_agent.py`

### 主要職責

- 定義 API 端點和路由
- 處理 HTTP 請求和響應
- 向客戶端提供清晰的接口

### 實現細節

```python
# router.py
router = APIRouter()
router.include_router(router=wikipedia_agent.router, prefix="/wikipedia", tags=["Wikipedia Agent"])

# wikipedia_agent.py - Your endpoint
@router.post("/", response_model=QueryResponse)
async def query_knowledge_base(
    request: QueryRequest,
    ai_service: AIService = Depends(get_ai_service)
):
```

路由層依賴注入服務層的實例，通過 FastAPI 的依賴注入系統獲取 `AIService` 的實例。

## 2. 服務層 (Service Layer)

位於 `porygon_api/app/agent/service.py` 和 `porygon_api/app/agent/dependencies.py`

### 主要職責

- 實現業務邏輯
- 管理模型的加載和使用
- 處理數據轉換和錯誤處理

### 實現細節

```python
# service.py - 實現 AI 服務邏輯
class AIService:
    _instance = None  # 單例模式
    _model = None     # 共享模型實例
    
    def __new__(cls):
        # 單例模式實現，確保只有一個服務實例
        # 預加載模型
    
    async def predict(self, request: QueryRequest):
        # 使用模型進行預測，處理結果

# dependencies.py - 提供依賴注入
def get_ai_service():
    global _rag_service
    if _rag_service is None:
        _rag_service = AIService()
    return _rag_service
```

服務層採用單例模式，確保整個應用中只有一個服務實例，避免重複加載模型。同時在服務初始化時預加載模型，提高首次請求的響應速度。

## 3. 模型層 (Model Layer)

模型層不是顯式的代碼層，而是通過 MLflow 集成實現的。

### 主要職責

- 加載和管理 AI 模型
- 提供模型推理功能
- 處理模型輸入和輸出格式

### 實現細節

```python
# 在 service.py 中加載模型
def _load_model_internal(self):
    if AIService._model is None:
        login_mlflow()  # 設置 MLflow 配置
        AIService._model = mlflow.pyfunc.load_model(self.model_uri)

# 使用模型進行預測
result = model.predict(model_input)
```

模型加載通過 MLflow 的 Python 客戶端 API 實現，這使得可以無縫集成不同類型的模型（如 Wikipedia 代理、聊天代理等）。

## 4. 數據層 (Schema Layer)

位於 `porygon_api/app/agent/schemas.py` 和 `porygon_api/schemas.py`

### 主要職責

- 定義請求和響應的數據結構
- 實現數據驗證邏輯
- 提供數據序列化和反序列化功能

### 實現細節

```python
# schemas.py - 定義 API 數據模型
class QueryRequest(BaseModel):
    query: str  # 用戶查詢

class PredictResponse(BaseModel):
    answers: str  # 模型回答

class QueryResponse(BaseResponse[List[PredictResponse]]):
    pass  # 繼承通用響應結構
```

使用 Pydantic 模型定義數據結構，提供自動類型轉換和驗證功能，確保數據符合預期格式。

## 5. 工具層 (Utils Layer)

位於 `porygon_api/utils.py`

### 主要職責

- 提供通用功能和工具方法
- 初始化日誌和其他系統配置
- 處理 MLflow 連接和認證

### 實現細節

```python
# utils.py - 通用功能
def init_logging():
    # 初始化日誌配置

def login_mlflow():
    # 設置 MLflow 追蹤和註冊 URI
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_REGISTRY_URI = os.getenv("MLFLOW_REGISTRY_URI")
    
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_registry_uri(MLFLOW_REGISTRY_URI)
```

工具層提供了整個應用程序中可重用的功能，如日誌配置、MLflow 連接等。

## 中間件層 (Middleware Layer)

位於 `porygon_api/middleware/auth.py` 和 `porygon_api/main.py`

### 主要職責

- 處理請求前/後的通用邏輯
- 實現認證和授權功能
- 記錄請求日誌和監控指標

### 實現細節

```python
# main.py - 註冊中間件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 記錄請求並處理響應

# auth.py - 認證中間件
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 驗證請求並處理授權
```

中間件層提供了橫切關注點的處理，如請求日誌、認證授權等，適用於所有請求。

## 數據流

下面是一個典型請求的數據流程：

1. 客戶端向 `/api/v1/porygon/agent/wikipedia/` 發送 POST 請求
2. 中間件層處理通用邏輯（日誌、認證等）
3. 路由層解析請求並調用相應的處理函數
4. 依賴注入系統提供 AIService 實例
5. 服務層使用預加載的模型處理請求
6. 模型層執行推理並返回結果
7. 服務層格式化模型輸出
8. 路由層將結果包裝為響應並返回給客戶端

## 關鍵設計模式

1. **單例模式**: 確保服務和模型只被實例化一次
2. **依賴注入**: 通過 FastAPI 的依賴系統提供服務實例
3. **預加載策略**: 在服務啟動時預加載模型，提高首次請求性能
4. **層次分離**: 明確的層次結構，每層有清晰的職責
5. **數據驗證**: 使用 Pydantic 模型進行請求和響應數據驗證

這種架構設計使得系統具有良好的可維護性、可擴展性和可靠性，同時通過模型預加載和單例模式優化了性能和資源使用。