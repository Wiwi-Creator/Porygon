import ray
import torch
import socket
import time


ray.init()   # 16384MiB


def check_gpu_memory(device):
    total_memory = torch.cuda.get_device_properties(device).total_memory  # GPU的總記憶體
    allocated_memory = torch.cuda.memory_allocated(device)
    free_memory = total_memory - allocated_memory  # 可用的記憶體
    total_memory_gib = total_memory / (1024**3)
    allocated_memory_gib = allocated_memory / (1024**3)
    free_memory_gib = free_memory / (1024**3)
    print(f"Total Memory: {total_memory_gib}, Allocated: {allocated_memory_gib}, Free: {free_memory_gib}")


@ray.remote(
    num_cpus=1,
    num_gpus=0.5
)
def gpu_intensive_task(task_id):  # 5345/16384 (MiB)
    #required_memory = 5 * 1024**3  # 假設每個任務需要 5GB 的 GPU 記憶體
    pod_ip = socket.gethostbyname(socket.gethostname())
    print(f"Task {task_id} started on GPU. Pod IP: {pod_ip}")
    device = torch.device("cuda")
    check_gpu_memory(device)
    batch_size = 20000
    a = torch.randn(batch_size, batch_size, device=device)
    b = torch.randn(batch_size, batch_size, device=device)
    result = torch.mm(a, b)
    check_gpu_memory(device)
    #time.sleep(50)
    print(f"Task {task_id} completed on GPU.")
    return result.cpu().numpy()


num_tasks = 50
futures = [gpu_intensive_task.remote(i) for i in range(num_tasks)]
ray.wait(futures, num_returns=len(futures))
print("All GPU tasks completed.")
