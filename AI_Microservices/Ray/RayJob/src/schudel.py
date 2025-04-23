import ray
import time
import torch


# 即使邏輯上正確的分配
@ray.remote(num_gpus=0.25, # 4 個任務共享 1 張GPU
            num_cpus=1,
            max_retries=-1)
def parallel_tasks():
    # 假設每個任務都可能用掉 5GB (GPU Memory) => 總共需 20 GB
    # 如果實際的 GPU 只有 16GB 就會出錯
    # Retry = -1 , 則是不斷重試 當其他任務完成後 資源釋放後變可以 retry 成功


# 解決方案: 配合其他套件來檢視實際的用量作 Try Except
def managed_gpu_task():
    device = torch.device("cuda")
    total_memory = torch.cuda.get_device_properties(device).total_memory
    allocated_memory = torch.cuda.memory_allocated(device)
    current_usage_fraction = allocated_memory / total_memory
    if current_usage_fraction > 0.5: # 如果 GPU 使用量 > 0.5 則繼續等待資源釋放
        print(f"Current GPU memory usage is {current_usage_fraction:.2f}, which is greater than 0.5. Sleeping...")
        time.sleep(30)
    else:
        print(f"Current GPU memory usage is {current_usage_fraction:.2f}, which is less than or equal to 0.5.")        
        pass
