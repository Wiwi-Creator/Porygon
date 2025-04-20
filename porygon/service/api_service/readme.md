# Porygon API 架構詳解

## Architecture

Porygon API 是一個基於 FastAPI 的服務，提供 AI 模型預測和資料庫查詢功能。架構採用清晰的分層設計：

1. **路由層 (Router Layer)**：處理 HTTP 請求路由和參數解析
2. **服務層 (Service Layer)**：實現業務邏輯和模型交互
3. **模型層 (Model Layer)**：加載和使用 AI 模型進行預測
4. **數據層 (Schema Layer)**：定義數據結構和驗證規則
5. **資料庫層 (Database Layer)**：與 Cloud SQL 和 Firestore 交互
6. **中間件層 (Middleware Layer)**：處理認證、日誌和請求追蹤
7. **監控與日誌層 (Monitoring & Logging)**：整合 Cloud Logging 和 BigQuery

## 路由層 (Router Layer)

位於 `porygon_api/app/AIservice/router.py` 和 `porygon_api/app/UserQuery/router.py`

### 主要職責

- 定義 API Endpoint 和 Router
- 處理 HTTP Request 和 Respones
- 向 Client 端提供 接口

### 實現細節

```python
# AIservice/router.py
router = APIRouter()
router.include_router(router=wikipedia_agent.router, prefix="/wikipedia_agent")

# UserQuery/router.py
router = APIRouter()
router.include_router(router=Item.router, prefix="/resource")
```

服務分為兩大功能模塊：
- **AIservice**: 提供基於MLflow中的Model作預測作推理
- **UserQuery**: 提供資料庫項目查詢功能

## 2. 服務層 (Service Layer)

Ex:  `porygon_api/app/AIservice/service.py` 和 `porygon_api/app/UserQuery/service.py`

### 職責

- 實現 主要的業務邏輯
- 處理數據轉換和錯誤處理
- 與資料庫交互

### 程式碼說明

```python
# AIservice/service.py
class AIService:
    _instance = None  # 單例模式

    async def predict(self, request: QueryRequest) -> List[PredictResponse]:
        # 使用模型進行預測

# UserQuery/service.py
class ItemService:
    _instance = None

    async def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        # 從 Cloud SQL 查詢 Item

    async def get_product(self, collection: str, product_id: str) -> Dict[str, Any]:
        # 從 Firestore 查詢 Product
```

服務層採用單例模式，確保系統資源高效利用。

## 3. 模型層 (Model Layer)

位於 `porygon_api/model_manager.py`

### 主要職責

- 加載和管理 AI 模型
- 提供模型推理功能
- 處理模型輸入和輸出格式

### 實現細節

```python
class ModelManager:
    _instance = None
    _lock = threading.Lock()
    
    def _preload_model(self):
        # 預加載模型
        self.model = mlflow.pyfunc.load_model(self.model_uri)
    
    def predict(self, data):
        # 使用模型進行預測
        result = model.predict(data)
```

模型管控透過 MLflow ，用來作 模型 的 加載、版本管理和監控。

## 4. 數據層 (Schema Layer)

位於 `porygon_api/app/AIservice/schemas.py` 和 `porygon_api/app/UserQuery/schemas.py`

### 職責

- 定義請求和響應的數據結構
- 實現數據驗證邏輯
- 提供數據序列化和反序列化功能

### 實現細節

```python
# AIservice/schemas.py
class QueryRequest(BaseModel):
    query: str

class PredictResponse(BaseModel):
    answers: str

# UserQuery/schemas.py
class ItemBase(BaseModel):
    name: str = Field(..., description="物品名稱")
    description: Optional[str] = Field(None, description="物品描述")
```

## 5. 資料庫層 (Database Layer)

位於 `porygon_api/database/db_connector.py`

### 主要職責

- 管理數據庫連接
- 提供數據庫操作接口
- 處理數據庫事務和錯誤

### 實現細節

```python
class CloudSQLConnector:
    _instance = None

    def connect(self):
        # 連接到 Cloud SQL

    def execute_query(self, query, params=None):
        # 執行 SQL 查詢

class FirestoreConnector:
    _instance = None

    def connect(self):
        # 連接到 Firestore
```

支持兩種數據庫：
- **Cloud SQL**: 用於關係式數據存儲
- **Firestore**: 用於 NoSQL 文檔存儲

## 6. 中間件層 (Middleware Layer)

位於 `porygon_api/middleware/`

### 主要職責

- 處理 請求前/後的通用邏輯
- 實現認證和授權功能 (Auth)
- 記錄請求日誌和監控指標

### 邏輯

```python
# auth.py
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 驗證 API Key

# http.py
class HttpMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 記錄請求處理時間和結果
```

中間件提供跨越多個請求的通用功能，如認證、性能監控等。

## 7. 監控與日誌層 (Monitoring & Logging)

### 主要職責

- 記錄系統日誌
- 監控系統性能
- 提供可視化分析數據

### 結構化日誌格式

所有日誌使用 JSON 格式輸出，包含以下字段：
- **timestamp**: 日誌時間
- **level**: 日誌級別
- **module**: 模塊名稱
- **line**: 代碼行號
- **message**: 日誌信息

### Cloud Logging 整合

應用自動將日誌發送到 Google Cloud Logging，無需額外配置。當部署到 Cloud Run 時，標準輸出會被自動收集。

### BigQuery 整合

設置 Log Sink 將日誌從 Cloud Logging 導出到 BigQuery，實現以下功能：
- 長期日誌存儲
- 複雜查詢分析
- 性能監控和異常檢測

### 示例查詢

```sql
-- 查詢端點性能
SELECT
  JSON_EXTRACT_SCALAR(jsonPayload, '$.path') AS endpoint,
  COUNT(*) AS request_count,
  AVG(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.process_time') AS FLOAT64)) AS avg_time
FROM
  `project_id.dataset.table`
WHERE
  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
GROUP BY
  endpoint
ORDER BY
  avg_time DESC;
```

## 部署架構

### 本地測試

使用以下command在本地運行該 API Service

```bash
gunicorn porygon_api.main:app \
  -k uvicorn.workers.UvicornWorker \
  --preload \
  --workers 4 \
  --bind 0.0.0.0:8080 \
  --timeout 120 \
  --keep-alive 120
```

### Cloud Run 部署

1. **構建 Docker 鏡像**：
   ```bash
   make build-m1 && make tag && make push
   ```

2. **部署到 Cloud Run**：
   ```bash
   gcloud run deploy "porygon-api" \
     --image="IMAGE_URL" \
     --platform=managed \
     --region="asia-east1" \
     --allow-unauthenticated \
     --port=8080 \
     --memory="4Gi" \
     --cpu=4
   ```

3. **環境變數設置**：
   - `GCP_PROJECT_ID`: GCP 項目 ID
   - `MODEL_URI`: MLflow 模型 URI
   - `MLFLOW_TRACKING_URI`: MLflow 追蹤服務器 URI

## API 端點

### AIservice 端點
1. Document UI: 

## 關鍵設計模式

1. **單例模式**: 確保服務和連接器只被實例化一次
2. **依賴注入**: 通過 FastAPI 的依賴系統提供服務實例
3. **中間件鏈**: 通過中間件鏈處理請求的通用邏輯
4. **預加載策略**: 在服務啟動時預加載模型，提高性能
5. **日誌集中化**: 將所有日誌集中到 Cloud Logging 和 BigQuery

## 安全性

- **API 密鑰認證**: 使用 X-API-Key head 進行認證
- **基於角色的訪問控制**: 不同角色擁有不同的端點訪問權限
- **請求 ID 追蹤**: 每個請求分配唯一 ID 用於跟踪和審計

## 日誌與監控最佳實踐

1. **結構化日誌**: 使用 JSON 格式確保日誌可以被有效解析和查詢
2. **包含上下文**: 在日誌中包含請求 ID、用戶 ID 等上下文信息
3. **性能指標**: 記錄請求處理時間等性能指標
4. **集中分析**: 將日誌導出到 BigQuery 進行深度分析
5. **設置警報**: 基於日誌數據設置異常Alert
