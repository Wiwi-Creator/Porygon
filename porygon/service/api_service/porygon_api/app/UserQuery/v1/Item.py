import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from porygon_api.app.UserQuery.schemas import (
    CreateItemRequest, CreateItemResponse,
    FirestoreItemRequest, FirestoreItemResponse
)
from porygon_api.app.UserQuery.dependencies import get_item_service
from porygon_api.app.UserQuery.service import ItemService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=CreateItemResponse)
async def create_item(
    request: CreateItemRequest,
    item_service: ItemService = Depends(get_item_service)
):
    """
    在 Cloud SQL 中創建新物品
    """
    try:
        logger.info(f"收到創建物品請求: {request.name}")
        result = await item_service.create_item(request)

        if not result.get("id"):
            logger.error("物品創建失敗")
            return CreateItemResponse(
                responseCode=500,
                responseMessage="物品創建失敗",
                results=result
            )

        logger.info(f"物品創建成功: {result.get('id')}")

        return CreateItemResponse(
            responseCode=201,
            responseMessage="物品創建成功",
            results=result
        )
    except Exception as e:
        logger.error(f"處理物品創建請求時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        # 返回一個空的字典
        empty_result = {
            "id": "",
            "name": "",
            "description": None,
            "price": 0.0,
            "quantity": 0,
            "category": None,
            "tags": None,
            "properties": None
        }
        
        return CreateItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results=empty_result
        )

@router.put("/{item_id}", response_model=CreateItemResponse)
async def update_item(
    item_id: str,
    request: CreateItemRequest,
    item_service: ItemService = Depends(get_item_service)
):
    """
    更新 Cloud SQL 中的物品
    Args:
        item_id: 物品 ID
        request: 更新物品請求
        item_service: 物品服務依賴注入

    Returns:
        更新響應，包含更新後的物品信息
    """
    try:
        logger.info(f"收到更新物品請求: {item_id}")
        result = await item_service.update_item(item_id, request)

        if not result.get("id"):
            logger.error(f"物品 {item_id} 更新失敗")
            return CreateItemResponse(
                responseCode=404,
                responseMessage=f"物品 {item_id} 更新失敗，可能不存在",
                results=result
            )

        logger.info(f"物品更新成功: {result.get('id')}")

        return CreateItemResponse(
            responseCode=200,
            responseMessage="Firestore 物品更新成功",
            results=result
        )
    except Exception as e:
        logger.error(f"處理物品更新請求時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        # 返回一個空的字典
        empty_result = {
            "id": "",
            "name": "",
            "description": None,
            "price": 0.0,
            "quantity": 0,
            "category": None,
            "tags": None,
            "properties": None
        }

        return CreateItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results=empty_result
        )


async def create_firestore_item(collection: str,document_id: str,request: CreateItemRequest,item_service: ItemService = Depends(get_item_service):
    """在 Firestore 中創建新物品

    Args:
        request: 物品資料和 Firestore 特定參數

    Returns:
        包含操作結果的字典
    """
    try:
        item_data = {
            "name": request.name,
            "description": request.description,
            "price": request.price,
            "quantity": request.quantity,
            "category": request.category
        }

        logger.info(f"準備在 Firestore 中創建物品: {request.name} 於集合 {request.collection}")

        result = await item_service.create_firestore_item(
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


@router.put("/firestore/{collection}/{document_id}", response_model=FirestoreItemResponse)
async def update_firestore_item(
    collection: str,
    document_id: str,
    request: CreateItemRequest,
    item_service: ItemService = Depends(get_item_service)
):
    """
    更新 Firestore 中的物品

    Args:
        collection: Firestore 集合名稱
        document_id: 文檔 ID
        request: 更新物品請求
        item_service: 物品服務依賴注入

    Returns:
        更新響應，包含操作結果
    """
    try:
        logger.info(f"收到 Firestore 物品更新請求: {document_id} 在集合 {collection}")

        # 準備更新數據
        update_data = request.model_dump(exclude_unset=True)

        # 更新 Firestore 物品
        result = await item_service.update_firestore_item(
            collection=collection,
            document_id=document_id,
            data=update_data
        )

        if result["status"] == "error":
            logger.error(f"Firestore 物品更新失敗: {result.get('message')}")
            return FirestoreItemResponse(
                responseCode=500,
                responseMessage=f"Firestore 物品更新失敗: {result.get('message')}",
                results=result
            )

        logger.info(f"Firestore 物品更新成功: {document_id}")

        return FirestoreItemResponse(
            responseCode=200,
            responseMessage="Firestore 物品更新成功",
            results=result
        )
    except Exception as e:
        logger.error(f"處理 Firestore 物品更新請求時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return FirestoreItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results={"status": "error", "message": str(e)}
        )
