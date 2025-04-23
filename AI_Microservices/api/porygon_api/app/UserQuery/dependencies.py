from porygon_api.app.UserQuery.service import ItemService

_item_service = None


def get_item_service():
    """
    提供物品服務的單例實例
    使用依賴注入確保數據庫會話可用，同時保持物品服務的單例狀態
    """
    global _item_service
    if _item_service is None:
        _item_service = ItemService()
    return _item_service
