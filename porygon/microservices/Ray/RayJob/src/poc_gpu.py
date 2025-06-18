import ray
import torch
import time


@ray.remote(
    num_cpus=0.1,
    num_gpus=0.2,
    retry_exceptions=True,
    max_retries=-1
    )
def gpu_intensive_task(task_id, size_in_gb):
    device = torch.device("cuda")
    num_elements = (size_in_gb * (1024**3)) // 4  # 4 bytes per float32
    _ = torch.empty(num_elements, dtype=torch.float32, device=device)
    time.sleep(5)
    print(f"Task {task_id} started on GPU. Allocated {size_in_gb} GB on GPU")
    time.sleep(5)


num_tasks = 100  # 執行 N 個並行任務
futures = [gpu_intensive_task.remote(i, 3) for i in range(num_tasks)]
results = ray.get(futures)
print("All GPU tasks completed.")
