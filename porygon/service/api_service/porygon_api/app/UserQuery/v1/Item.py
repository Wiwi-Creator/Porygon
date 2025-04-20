import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from porygon_api.app.UserQuery.schemas import (
    CreateItemRequest, CreateItemResponse,
    FirestoreItemRequest, FirestoreItemResponse,
    ItemResponse
)
from porygon_api.app.UserQuery.dependencies import get_item_service
from porygon_api.app.UserQuery.service import ItemService
from porygon_api.schemas import BaseResponse

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


@router.get("/{item_id}", response_model=BaseResponse[ItemResponse])
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


@router.post("/firestore", response_model=FirestoreItemResponse)
async def create_firestore_item(
    request: FirestoreItemRequest,
    item_service: ItemService = Depends(get_item_service)
):
    """在 Firestore 中創建新物品

    Args:
        request: 物品資料和 Firestore 特定參數

    Returns:
        包含操作結果的字典
    """
    try:
        logger.info(f"準備在 Firestore 中創建物品: {request.name} 於集合 {request.collection}")

        # 將 request 轉換成適合 create_firestore_item 的參數
        result = await item_service.create_firestore_item(request)

        logger.info(f"Firestore 物品創建結果: {result}")
        
        if result.get("status") == "error":
            return FirestoreItemResponse(
                responseCode=500,
                responseMessage=f"Firestore 物品創建失敗: {result.get('message')}",
                results=result
            )
            
        return FirestoreItemResponse(
            responseCode=201,
            responseMessage="Firestore 物品創建成功",
            results=result
        )

    except Exception as e:
        logger.error(f"創建 Firestore 物品時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return FirestoreItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results={"status": "error", "message": str(e)}
        )


@router.get("/firestore/{collection}/{document_id}", response_model=FirestoreItemResponse)
async def get_firestore_item(
    collection: str,
    document_id: str,
    item_service: ItemService = Depends(get_item_service)
):
    """
    從 Firestore 獲取特定物品
    
    Args:
        collection: Firestore 集合名稱
        document_id: 文檔 ID
        item_service: 物品服務依賴注入
        
    Returns:
        包含物品數據的響應
    """
    try:
        logger.info(f"收到 Firestore 物品查詢請求: {document_id} 在集合 {collection}")
        
        result = await item_service.get_firestore_item(
            collection=collection,
            document_id=document_id
        )
        
        if result.get("status") == "error":
            logger.error(f"Firestore 物品查詢失敗: {result.get('message')}")
            return FirestoreItemResponse(
                responseCode=404,
                responseMessage=f"未找到物品: {result.get('message')}",
                results=result
            )
            
        logger.info(f"成功獲取 Firestore 物品: {document_id}")
        
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
