import csv
import threading
import time

with open("tasks_4.csv", "w") as f:
    f.write(
        "task_id,thread_name,burst_ms,priority,status\n"
        "T1,Worker_1,100,HIGH,PENDING\n"
        "T2,Worker_2,150,MEDIUM,PENDING\n"
        "T3,Worker_1,80,LOW,PENDING\n"
    )

mutex=threading.Lock()
completed_task=[]

def execute_task(task_id,burst_ms,thread_name):
    print(f"[{thread_name}] Waiting to acquire lock for {task_id}...")
    with mutex:
        print(f"[{thread_name}] LOCK ACQUIRED -> Executing {task_id}")
        time.sleep(burst_ms/1000.0)
        completed_task
        .append(task_id)
        print(f"[{thread_name}] LOCK RELEASED -> Finished {task_id}")

threads=[]
with open("tasks_4.csv","r") as f:
    for row in csv.DictReader(f):
        t=threading.Thread(
            target=execute_task,
            args=(row["task_id"],float(row["burst_ms"]),row["thread_name"])
        )
        threads.append(t)
        t.start()

for t in threads:
    t.join()

print("\nFinal completed task list:", completed_task) 