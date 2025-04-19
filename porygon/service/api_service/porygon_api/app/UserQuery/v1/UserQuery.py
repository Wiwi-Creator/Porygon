import logging
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
    
    Args:
        request: 物品創建請求
        item_service: 物品服務依賴注入
        
    Returns:
        創建響應，包含新物品信息
    """
    try:
        logger.info(f"收到創建物品請求: {request.name}")
        
        # 創建物品
        result = await item_service.create_item(request)
        
        if not result:
            logger.error("物品創建失敗")
            return CreateItemResponse(
                responseCode=500,
                responseMessage="物品創建失敗",
                results=None
            )
        
        logger.info(f"物品創建成功: {result['id']}")
        
        return CreateItemResponse(
            responseCode=201,
            responseMessage="物品創建成功",
            results=result
        )
    except Exception as e:
        logger.error(f"處理物品創建請求時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return CreateItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results=None
        )


@router.post("/firestore", response_model=FirestoreItemResponse)
async def create_firestore_item(
    request: FirestoreItemRequest,
    item_service: ItemService = Depends(get_item_service)
):
    """
    在 Firestore 中創建新物品
    
    Args:
        request: Firestore 物品創建請求
        item_service: 物品服務依賴注入
        
    Returns:
        創建響應，包含操作結果
    """
    try:
        logger.info(f"收到 Firestore 物品創建請求: {request.name} 在集合 {request.collection}")
        
        # 創建 Firestore 物品
        result = await item_service.create_firestore_item(request)
        
        if result["status"] == "error":
            logger.error(f"Firestore 物品創建失敗: {result.get('message')}")
            return FirestoreItemResponse(
                responseCode=500,
                responseMessage=f"Firestore 物品創建失敗: {result.get('message')}",
                results=result
            )
        
        logger.info(f"Firestore 物品創建成功: {result.get('document_id')}")
        
        return FirestoreItemResponse(
            responseCode=201,
            responseMessage="Firestore 物品創建成功",
            results=result
        )
    except Exception as e:
        logger.error(f"處理 Firestore 物品創建請求時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return FirestoreItemResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results={"status": "error", "message": str(e)}
        )


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
