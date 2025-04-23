from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from porygon_api.schemas import BaseResponse


class ItemBase(BaseModel):
    """基本物品資料模型"""
    name: str = Field(..., description="物品名稱")
    description: Optional[str] = Field(None, description="物品描述")
    price: float = Field(..., description="物品價格")
    quantity: int = Field(..., description="物品數量")
    category: Optional[str] = Field(None, description="物品類別")


class ItemResponse(BaseModel):
    """物品資料回應模型"""
    id: str
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: Optional[str] = None
    tags: Optional[list] = None
    properties: Optional[Dict[str, Any]] = None


class FirestoreItemResponse(BaseResponse[Dict[str, Any]]):
    """Firestore 操作回應"""
    pass
