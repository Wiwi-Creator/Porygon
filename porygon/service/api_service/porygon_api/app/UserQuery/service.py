import logging
import uuid
from typing import Dict, Any, Optional
from google.cloud import firestore

from porygon_api.app.UserQuery.schemas import FirestoreItemRequest
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
    async def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """從 Cloud SQL 獲取特定物品
    
        Args:
            item_id: 物品 ID
    
        Returns:
            包含物品數據的字典，如果未找到則返回 None
        """
        try:
            # 使用命名參數的 SQL 查詢
            query = """
            SELECT id, name, description, price, quantity, category
            FROM items
            WHERE id = :id
            """
    
            # 參數字典
            params = {"id": item_id}
    
            logger.info(f"準備從 Cloud SQL 查詢物品: {item_id}")
            result = cloud_sql_connector.execute_query(query, params)
    
            if result["status"] == "success" and "data" in result and result["data"]:
                item = result["data"][0]
                logger.info(f"成功獲取物品: {item_id}")
    
                # 將缺失的屬性設置為 None
                item.setdefault("tags", None)
                item.setdefault("properties", None)
    
                return item
            else:
                logger.error(f"未找到物品: {item_id}")
                return None
    
        except Exception as e:
            logger.error(f"查詢物品時發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    
    async def get_firestore_item(self, collection: str, document_id: str) -> Dict[str, Any]:
        """從 Firestore 獲取特定物品
        Args:
            collection: Firestore 集合名稱
            document_id: 文檔 ID
        Returns:
            包含物品數據的字典或錯誤信息
        """
        try:
            logger.info(f"準備從 Firestore 獲取物品: {document_id} 從集合 {collection}")
    
            # 獲取 Firestore 客戶端
            client = firestore_connector.connect()
    
            # 獲取文檔引用
            doc_ref = client.collection(collection).document(document_id)
            doc = doc_ref.get()
    
            if doc.exists:
                logger.info(f"成功從 Firestore 獲取物品: {document_id}")
                item_data = doc.to_dict()
                # 添加文檔 ID 到返回數據
                item_data["id"] = document_id
                return {
                    "status": "success",
                    "data": item_data
                }
            else:
                logger.error(f"Firestore 中未找到物品: {document_id}")
                return {
                    "status": "error",
                    "message": f"未找到文檔 {document_id}"
                }
    
        except Exception as e:
            logger.error(f"從 Firestore 獲取物品時發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }
    