#!/bin/bash

echo "=== MLflow 容器權限診斷 ==="

# 檢查容器是否運行
if ! docker ps | grep -q "mlflow-server"; then
    echo "❌ MLflow 容器未運行，請先啟動容器"
    exit 1
fi

echo "✅ MLflow 容器正在運行"

# 檢查容器內的權限和目錄結構
echo -e "\n1. 檢查容器內 /app 目錄權限:"
docker exec mlflow-server ls -la /app/

echo -e "\n2. 檢查容器運行用戶:"
docker exec mlflow-server whoami
docker exec mlflow-server id

echo -e "\n3. 檢查 /app 目錄的所有者和權限:"
docker exec mlflow-server stat /app

echo -e "\n4. 測試寫入權限:"
docker exec mlflow-server touch /app/test_write_permission 2>&1 && echo "✅ /app 可寫" || echo "❌ /app 不可寫"

echo -e "\n5. 檢查 mlartifacts 目錄:"
docker exec mlflow-server ls -la /app/mlartifacts/ 2>/dev/null || echo "/app/mlartifacts 不存在或無權限"
docker exec mlflow-server touch /app/mlartifacts/test_write 2>&1 && echo "✅ mlartifacts 可寫" || echo "❌ mlartifacts 不可寫"

echo -e "\n6. 檢查臨時目錄權限:"
docker exec mlflow-server touch /tmp/test_temp_write 2>&1 && echo "✅ /tmp 可寫" || echo "❌ /tmp 不可寫"

echo -e "\n7. 檢查容器內的掛載點:"
docker exec mlflow-server mount | grep /app

echo -e "\n8. 檢查文件系統類型:"
docker exec mlflow-server df -T /app

echo -e "\n=== 清理測試文件 ==="
docker exec mlflow-server rm -f /app/test_write_permission /app/mlartifacts/test_write /tmp/test_temp_write 2>/dev/null
echo "診斷完成"