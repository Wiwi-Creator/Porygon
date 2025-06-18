import logging
from typing import Dict, Any, Optional

from porygon_api.database.db_connector import cloud_sql_connector, firestore_connector

logger = logging.getLogger(__name__)


class ItemService:
    """提供搜尋資料庫服務，提供對 Cloud SQL 和 Firestore 的操作"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating ItemService singleton instance")
            cls._instance = super(ItemService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        logger.info("Initializing ItemService")
        self._initialized = True

    async def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific item from Cloud SQL.

        Args:
            item_id: The ID of the item.

        Returns:
            A dictionary containing item data if found, otherwise None.
        """
        try:
            # SQL query using named parameters
            query = """
            SELECT id, name, description, price, quantity, category
            FROM items
            WHERE id = :id
            """

            # Parameter dictionary
            params = {"id": item_id}

            logger.info(f"Querying Cloud SQL for item: {item_id}")
            result = cloud_sql_connector.execute_query(query, params)

            if result["status"] == "success" and "data" in result and result["data"]:
                item = result["data"][0]
                logger.info(f"Successfully retrieved item: {item_id}")

                # Set missing optional fields to None
                item.setdefault("tags", None)
                item.setdefault("properties", None)

                return item
            else:
                logger.error(f"Item not found: {item_id}")
                return None

        except Exception as e:
            logger.error(f"Error occurred while querying item: {str(e)}")
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
            logger.info(f"Querying Firestore collection '{collection}' for product_id: {product_id}")
            client = firestore_connector.connect()
            docs = (
                client.collection(collection)
                .where("Product_id", "==", product_id)
                .stream()
            )
            doc = next(docs, None)

            if doc and doc.exists:
                logger.info(f"Successfully retrieved product_id: {product_id} from Firestore")
                item_data = doc.to_dict()
                item_data["id"] = doc.id
                return {
                    "status": "success",
                    "data": item_data
                }
            else:
                logger.error(f"No document found in Firestore with product_id: {product_id}")
                return {
                    "status": "error",
                    "message": f"No document found with product_id: {product_id}"
                }

        except Exception as e:
            logger.error(f"Error occurred while querying Firestore with product_id: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }
