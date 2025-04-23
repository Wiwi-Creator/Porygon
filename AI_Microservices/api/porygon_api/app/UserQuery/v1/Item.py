import logging
from fastapi import APIRouter, Depends

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
        logger.info(f"Get Item Resuest: {item_id}")
        result = await item_service.get_item(item_id)
        if not result or not result.get("id"):
            logger.error(f"Item Not Found: {item_id}")
            return BaseResponse[ItemResponse](
                responseCode=404,
                responseMessage=f"Item with ID with {item_id} Not Found.",
                results=None
            )

        logger.info(f"Got Item Successfully : {item_id}")

        return BaseResponse[ItemResponse](
            responseCode=200,
            responseMessage="Got Item Successfully.",
            results=result
        )
    except Exception as e:
        logger.error(f"Error occurred while searching items: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return BaseResponse[ItemResponse](
            responseCode=500,
            responseMessage=f"Failed to process request: {str(e)}",
            results=None
        )


@router.get("/GetProducts/{collection}/{product_id}", response_model=FirestoreItemResponse)
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
        logger.info(f"Got Product request: {product_id} on collection: {collection}")

        result = await item_service.get_product(
            collection=collection,
            product_id=product_id
        )

        if result.get("status") == "error":
            logger.error(f"Failed to query Product: {result.get('message')}")
            return FirestoreItemResponse(
                responseCode=404,
                responseMessage=f"Product not found: {result.get('message')}",
                results=result
            )

        logger.info(f"Get Firestore objects successfully : {product_id}")

        return FirestoreItemResponse(
            responseCode=200,
            responseMessage="Get Product successfully.",
            results=result
        )

    except Exception as e:
        logger.error(f"Error occurred while searching product: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return FirestoreItemResponse(
            responseCode=500,
            responseMessage=f"Error message: {str(e)}",
            results={"status": "error", "message": str(e)}
        )
