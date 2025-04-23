import ray
import torch
import time


ray.init()


@ray.remote(
    num_cpus=1,
    num_gpus=0.2,  # Ray會 設定 CUDA_VISIBLE_DEVICES , 不會限制 GPU Memory 使用量
    # resources={"GPU_MEMORY": 4} # 自定義資源
    )
def gpu_intensive_task(task_id):   # 實際用量 4GiB
    print(f"Task {task_id} started on GPU.")
    device = torch.device("cuda")
    batch_size = 16000
    torch.cuda.empty_cache()
    a = torch.randn(batch_size, batch_size, device=device)
    b = torch.randn(batch_size, batch_size, device=device)
    result = torch.mm(a, b)
    print(f"Task {task_id} completed on GPU.")
    time.sleep(40)
    return result.cpu().numpy()


num_tasks = 100  # 執行 N 個並行任務
futures = [gpu_intensive_task.remote(i) for i in range(num_tasks)]
results = ray.get(futures)

print("All GPU tasks completed.")
