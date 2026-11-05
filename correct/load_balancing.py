import csv

# 1. Setup Dataset[cite: 2]
with open("workload_5.csv", "w") as f:
    f.write(
        "job_id,compute_units,assigned_worker,status\n"
        "J101,35,UNASSIGNED,PENDING\n"
        "J102,50,UNASSIGNED,PENDING\n"
        "J103,15,UNASSIGNED,PENDING\n"
        "J104,40,UNASSIGNED,PENDING\n"
    )

# 2. Workers and Least-Connections Scheduling[cite: 2]
workers = {"Worker_1": 0, "Worker_2": 0, "Worker_3": 0}
allocations = []

with open("workload_5.csv", "r") as f:
    for row in csv.DictReader(f):
        jid = row["job_id"]
        units = int(row["compute_units"])

        # Pick worker with least assigned load
        least_loaded_worker = min(workers, key=workers.get)
        workers[least_loaded_worker] += units

        allocations.append((jid, least_loaded_worker, units))
        print(
            f"[ALLOCATION] Job {jid} ({units} units) -> Assigned to {least_loaded_worker}"
        )  #[cite: 2]
        print(f"             Current load per worker: {workers}")  #[cite: 2]

print("\nBalanced summary of tasks across all worker nodes:")  #[cite: 2]
for worker, total in workers.items():
    print(f"  {worker}: Total Compute Units = {total}")