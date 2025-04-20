import logging
import uuid
from typing import Dict, Any
from google.cloud import firestore

from porygon_api.app.UserQuery.schemas import ItemBase, FirestoreItemRequest, ItemResponse
from porygon_api.database.db_connector import cloud_sql_connector, firestore_connector


logger = logging.getLogger(__name__)


class ItemService:
    """物品服務，提供對 Cloud SQL 和 Firestore 的操作"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("創建 ItemService 單例")
            cls._instance = super(ItemService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        logger.info("初始化 ItemService")
        self._initialized = True

    async def create_item(self, item: ItemBase) -> Dict[str, Any]:
        """在 Cloud SQL 中創建新物品"""
        try:
            # 生成唯一 ID
            item_id = str(uuid.uuid4())

            # 使用命名參數的 SQL 查詢
            query = """
            INSERT INTO items (id, name, description, price, quantity, category)
            VALUES (:id, :name, :description, :price, :quantity, :category)
            RETURNING id, name, description, price, quantity, category
            """

            # 參數字典
            params = {
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "quantity": item.quantity,
                "category": item.category
            }

            logger.info(f"準備在 Cloud SQL 中創建物品: {item.name}")
            result = cloud_sql_connector.execute_query(query, params)

            if result["status"] == "success" and "data" in result:
                created_item = result["data"][0] if result["data"] else None
                logger.info(f"物品創建成功: {item_id}")
                return created_item
            else:
                logger.error(f"物品創建失敗: {result.get('message', '未知錯誤')}")
                return {
                    "id": "",
                    "name": "",
                    "description": None,
                    "price": 0.0,
                    "quantity": 0,
                    "category": None
                }

        except Exception as e:
            logger.error(f"創建物品時發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "id": "",
                "name": "",
                "description": None,
                "price": 0.0,
                "quantity": 0,
                "category": None
            }

    async def create_firestore_item(self, request: FirestoreItemRequest) -> Dict[str, Any]:
        """在 Firestore 中創建新物品

        Args:
            request: 物品資料和 Firestore 特定參數

        Returns:
            包含操作結果的字典
        """
        try:
            # 準備文檔資料
            item_data = {
                "name": request.name,
                "description": request.description,
                "price": request.price,
                "quantity": request.quantity,
                "category": request.category,
                "tags": request.tags,
                "properties": request.properties
            }

            logger.info(f"準備在 Firestore 中創建物品: {request.name} 於集合 {request.collection}")

            # 新增到 Firestore
            result = firestore_connector.add_document(
                collection=request.collection,
                data=item_data,
                document_id=request.document_id
            )

            logger.info(f"Firestore 物品創建結果: {result}")
            return result

        except Exception as e:
            logger.error(f"創建 Firestore 物品時發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}
    
    async def update_firestore_item(self, collection: str, document_id: str, 
                                   data: Dict[str, Any]) -> Dict[str, Any]:
        """更新 Firestore 中的物品

        Args:
            collection: Firestore 集合名稱
            document_id: 文檔 ID
            data: 更新資料

        Returns:
            包含操作結果的字典
        """
        try:
            logger.info(f"準備更新 Firestore 中的物品: {document_id} 於集合 {collection}")

            # 更新時添加時間戳
            update_data = dict(data)
            update_data["updated_at"] = firestore.SERVER_TIMESTAMP

            # 更新 Firestore 文檔
            result = firestore_connector.update_document(
                collection=collection,
                document_id=document_id,
                data=update_data
            )

            logger.info(f"Firestore 物品更新結果: {result}")
            return result

        except Exception as e:
            logger.error(f"更新 Firestore 物品時發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}
