import csv
import threading
import time

# 1. Setup Dataset[cite: 1]
with open("tasks_4.csv", "w") as f:
    f.write(
        "task_id,thread_name,burst_ms,priority,status\n"
        "T1,Worker_1,100,HIGH,PENDING\n"
        "T2,Worker_2,150,MEDIUM,PENDING\n"
        "T3,Worker_1,80,LOW,PENDING\n"
    )

# 2. Mutex & Shared Resources[cite: 1]
mutex = threading.Lock()
completed_tasks = []


def execute_task(task_id, thread_name, burst_ms):
    print(f"[{thread_name}] Waiting to acquire lock for {task_id}...")
    with mutex:  # Lock acquisition and automatic release[cite: 1]
        print(f"[{thread_name}] LOCK ACQUIRED -> Executing {task_id}")
        time.sleep(burst_ms / 1000.0)  # Simulate execution
        completed_tasks.append(task_id)
        print(f"[{thread_name}] LOCK RELEASED -> Finished {task_id}")


# 3. Read CSV and launch concurrent threads[cite: 1]
threads = []
with open("tasks_4.csv", "r") as f:
    for row in csv.DictReader(f):
        t = threading.Thread(
            target=execute_task,
            args=(row["task_id"], row["thread_name"], float(row["burst_ms"])),
        )
        threads.append(t)
        t.start()

for t in threads:
    t.join()

print("\nFinal completed task list:", completed_tasks)  #[cite: 1]