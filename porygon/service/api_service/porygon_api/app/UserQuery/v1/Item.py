import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from porygon_api.app.UserQuery.schemas import FirestoreItemResponse, ItemResponse

from porygon_api.app.UserQuery.dependencies import get_item_service
from porygon_api.app.UserQuery.service import ItemService
from porygon_api.schemas import BaseResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/GetItems/{item_id}", response_model=BaseResponse[ItemResponse])
async def get_item(
    item_id: str,
    item_service: ItemService = Depends(get_item_service)
):
    """
    根據 ID 從 Cloud SQL 獲取物品
    Args:
        item_id: 物品 ID
        item_service: 物品服務依賴注入
    Returns:
        包含物品信息的響應
    """
    try:
        logger.info(f"收到查詢物品請求: {item_id}")
        result = await item_service.get_item(item_id)
        if not result or not result.get("id"):
            logger.error(f"未找到物品: {item_id}")
            return BaseResponse[ItemResponse](
                responseCode=404,
                responseMessage=f"未找到 ID 為 {item_id} 的物品",
                results=None
            )

        logger.info(f"成功獲取物品: {item_id}")

        return BaseResponse[ItemResponse](
            responseCode=200,
            responseMessage="成功獲取物品",
            results=result
        )
    except Exception as e:
        logger.error(f"獲取物品時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return BaseResponse[ItemResponse](
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results=None
        )


@router.get("/GetProducts/{collection}/{document_id}", response_model=FirestoreItemResponse)
async def get_firestore_item(
    collection: str,
    product_id: str,
    item_service: ItemService = Depends(get_item_service)
):
    """
    從 Firestore 獲取特定物品

    Args:
        collection: Firestore 集合名稱
        product_id: 產品 ID
        item_service: 物品服務依賴注入

    Returns:
        包含物品數據的響應
    """
    try:
        logger.info(f"收到 Firestore 物品查詢請求: {product_id} 在集合 {collection}")

        result = await item_service.get_product(
            collection=collection,
            product_id=product_id
        )

        if result.get("status") == "error":
            logger.error(f"Firestore 物品查詢失敗: {result.get('message')}")
            return FirestoreItemResponse(
                responseCode=404,
                responseMessage=f"未找到物品: {result.get('message')}",
                results=result
            )

        logger.info(f"成功獲取 Firestore 物品: {product_id}")
        
        return FirestoreItemResponse(
            responseCode=200,
            responseMessage="成功獲取 Firestore 物品",
            results=result
        )

    except Exception as e:
        logger.error(f"獲取 Firestore 物品時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return FirestoreItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results={"status": "error", "message": str(e)}
        )
