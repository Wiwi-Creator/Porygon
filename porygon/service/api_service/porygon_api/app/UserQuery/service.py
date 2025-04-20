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

    async def get_product(self, collection: str, product_id: str) -> Dict[str, Any]:
        """根據自定義欄位 product_id 從 Firestore 獲取特定物品

        Args:
            collection: Firestore 集合名稱
            product_id: 自定義欄位，用來查詢產品

        Returns:
            包含物品數據的字典或錯誤信息
        """
        try:
            logger.info(f"準備從 Firestore 透過 product_id: {product_id} 查詢集合: {collection}")
            client = firestore_connector.connect()
            docs = (
                client.collection(collection)
                .where("Product_id", "==", product_id)
                .stream()
            )
            doc = next(docs, None)

            if doc and doc.exists:
                logger.info(f"成功從 Firestore 查到 product_id: {product_id}")
                item_data = doc.to_dict()
                item_data["id"] = doc.id  # 加入 firestore 文件 ID
                return {
                    "status": "success",
                    "data": item_data
                }
            else:
                logger.error(f"Firestore 中找不到 product_id 為 {product_id} 的文件")
                return {
                    "status": "error",
                    "message": f"找不到 product_id 為 {product_id} 的文件"
                }

        except Exception as e:
            logger.error(f"從 Firestore 查詢 product_id 時發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }
