##berkeley

import csv

# 1. Setup Dataset[cite: 1]
with open("node_clocks_3.csv", "w") as f:
    f.write(
        "node_id,clock_time_sec,is_faulty\n"
        "N1,3600,FALSE\n"
        "N2,3605,FALSE\n"
        "N3,3595,FALSE\n"
        "N4,4200,TRUE\n"  # Outlier/faulty[cite: 1]
    )

# 2. Polling and Outlier Elimination[cite: 1]
nodes = []
with open("node_clocks_3.csv", "r") as f:
    for row in csv.DictReader(f):
        nodes.append(
            {
                "id": row["node_id"],
                "time": float(row["clock_time_sec"]),
                "faulty": row["is_faulty"].strip().upper() == "TRUE",
            }
        )

print("Polled node times:", {n["id"]: n["time"] for n in nodes})  #[cite: 1]

# Discard faulty / outliers[cite: 1]
valid_nodes = [n for n in nodes if not n["faulty"]]
discarded = [n["id"] for n in nodes if n["faulty"]]
print(f"Identified and discarded outlier times: {discarded}")  #[cite: 1]

# Compute average[cite: 1]
avg_time = sum(n["time"] for n in valid_nodes) / len(valid_nodes)
print(f"Calculated average time: {avg_time:.2f} sec")  #[cite: 1]

# Relative adjustments[cite: 1]
print("\nRelative adjustment per node:")  #[cite: 1]
for n in valid_nodes:
    adj = avg_time - n["time"]
    print(f"  Node {n['id']}: Clock = {n['time']}, Adjustment = {adj:+.2f} sec")

##bully

import csv

# 1. Create dataset file: bully_cluster_2.csv
csv_content = """node_id,is_alive,is_current_coordinator
1,TRUE,FALSE
2,TRUE,FALSE
3,TRUE,FALSE
4,FALSE,FALSE
5,FALSE,TRUE"""

with open("bully_cluster_2.csv", "w") as f:
    f.write(csv_content)

# 2. Read nodes from CSV
cluster = {}
coordinator = None

with open("bully_cluster_2.csv", "r") as f:
    for row in csv.DictReader(f):
        nid = int(row["node_id"])
        alive = row["is_alive"].strip().upper() == "TRUE"
        is_coord = row["is_current_coordinator"].strip().upper() == "TRUE"
        cluster[nid] = alive
        if is_coord:
            coordinator = nid

# 3. Detect failure and run Bully Election
initiator = 2
if not cluster[coordinator]:
    print(f"Coordinator Node {coordinator} failed.")
    print(f"Node {initiator} detects failure and starts election.\n")

    current = initiator
    while True:
        higher_nodes = [nid for nid in cluster if nid > current]
        responded = []

        for h in higher_nodes:
            print(f"Initiator Node {current} sending ELECTION to Node {h}")
            if cluster[h]:
                print(f"Node {h} responding with OK")
                responded.append(h)

        if responded:
            current = max(responded)
            print()
        else:
            # Highest alive node becomes leader
            print(f"\nNode {current} won the election.")
            for nid in cluster:
                if nid != current and cluster[nid]:
                    print(f"Node {current} broadcasting COORDINATOR to Node {nid}")
            break

## cristian

import csv

# 1. Setup Dataset
with open("cristian_clocks_8.csv", "w") as f:
    f.write(
        "client_id,t0_send_ms,t_server_ms,tl_recv_ms\n"
        "C1,1000,1050,1100\n"
        "C2,2000,2080,2120\n"
    )

# 2. Cristian's Clock Synchronization Calculation
with open("cristian_clocks_8.csv", "r") as f:
    for row in csv.DictReader(f):
        cid = row["client_id"]
        t0 = float(row["t0_send_ms"])
        t_server = float(row["t_server_ms"])
        t1 = float(row["tl_recv_ms"])

        rtt = t1 - t0  # Round-trip time
        estimated_server_time = t_server + (rtt / 2.0)  #[cite: 2]
        offset = estimated_server_time - t1  #[cite: 2]

        print(f"Client: {cid}")
        print(f"  Calculated RTT = (T1 - T0) = {rtt:.2f} ms")  #[cite: 2]
        print(
            f"  Estimated Server Time = T_server + (RTT/2) = {estimated_server_time:.2f} ms"
        )  #[cite: 2]
        print(f"  Local Clock Offset Adjustment = {offset:+.2f} ms\n")  #[cite: 2]

## lamport

import csv

# 1. Setup Dataset[cite: 2]
with open("events_7.csv", "w") as f:
    f.write(
        "event_id,process_id,event_type,message_to,initial_clock\n"
        "E1,P1,SEND,P2,0\n"
        "E2,P2,RECV,P1,0\n"
        "E3,P1,INTERNAL,,0\n"
        "E4,P2,INTERNAL,,0\n"
    )

# 2. Process Lamport Logical Clocks[cite: 2]
clocks = {"P1": 0, "P2": 0}
message_timestamps = {}
event_log = []

with open("events_7.csv", "r") as f:
    for row in csv.DictReader(f):
        eid = row["event_id"]
        pid = row["process_id"]
        etype = row["event_type"].strip().upper()
        target = row["message_to"].strip()

        if etype == "SEND":
            clocks[pid] += 1
            message_timestamps[eid] = clocks[pid]
            print(
                f"[EVENT {eid}] {pid} SEND -> Clock updated to {clocks[pid]}"
            )
        elif etype == "RECV":
            # Rule: L = max(L, T_msg) + 1[cite: 2]
            t_msg = message_timestamps.get("E1", 0)
            clocks[pid] = max(clocks[pid], t_msg) + 1
            print(
                f"[EVENT {eid}] {pid} RECV using L=max(L, T_msg)+1 -> max({clocks[pid]-1}, {t_msg})+1 = {clocks[pid]}"
            )  #[cite: 2]
        else:
            clocks[pid] += 1
            print(
                f"[EVENT {eid}] {pid} INTERNAL -> Clock updated to {clocks[pid]}"
            )

        event_log.append({"event_id": eid, "pid": pid, "timestamp": clocks[pid]})

# Final Causal Ordering[cite: 2]
event_log.sort(key=lambda x: (x["timestamp"], x["pid"]))
print(
    "\nFinal sorted causal order of all events:",
    [e["event_id"] for e in event_log],
) 

##load balancing

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

##mpi

from concurrent.futures import ThreadPoolExecutor
import csv

# 1. Setup Dataset (Master Matrix A: 4x4)[cite: 4]
with open("matrix_22.csv", "w") as f:
    f.write(
        "row_id,col_0,col_1,col_2,col_3\n"
        "R0,2,4,1,5\n"
        "R1,1,3,0,2\n"
        "R2,3,1,2,4\n"
        "R3,0,2,5,1\n"
    )

# Target Vector / Matrix B Column
vector_B = [1, 2, 3, 4]


# 2. Worker Task (Row Dot Product)[cite: 4]
def worker_dot_product(task):
    row_id, row_vals = task
    res = sum(x * y for x, y in zip(row_vals, vector_B))
    print(f"[WORKER] Computed partial dot product for {row_id} = {res}")  #[cite: 4]
    return row_id, res


# 3. Read Matrix from CSV[cite: 4]
matrix_A = []
with open("matrix_22.csv", "r") as f:
    for row in csv.DictReader(f):
        r_vals = [
            int(row["col_0"]),
            int(row["col_1"]),
            int(row["col_2"]),
            int(row["col_3"]),
        ]
        matrix_A.append((row["row_id"], r_vals))

# 4. Master Scatter -> Worker Execution -> Master Gather[cite: 4]
print(f"[MASTER] Scattering {len(matrix_A)} matrix rows to worker tasks...")  #[cite: 4]
final_product = {}

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(worker_dot_product, matrix_A)
    for r_id, dot in results:
        final_product[r_id] = dot

print("\n[MASTER GATHER] Final matrix product result vector:")  #[cite: 4]
for r_id in sorted(final_product.keys()):
    print(f"  {r_id}: {final_product[r_id]}")

##multithreading

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

##ring

import csv

# 1. Setup Dataset
with open("ring_nodes_15.csv", "w") as f:
    f.write(
        "node_id,next_node_id,is_active,priority_rank\n"
        "1,2,TRUE,85\n"
        "2,3,TRUE,90\n"
        "3,4,TRUE,75\n"
        "4,5,FALSE,99\n"  # Coordinator failed[cite: 4]
        "5,1,TRUE,60\n"
    )

# 2. Read Ring Structure[cite: 4]
ring = {}
with open("ring_nodes_15.csv", "r") as f:
    for row in csv.DictReader(f):
        ring[int(row["node_id"])] = {
            "next": int(row["next_node_id"]),
            "active": row["is_active"].strip().upper() == "TRUE",
            "priority": int(row["priority_rank"]),
        }

# 3. Detect failure and circulate election token[cite: 4]
initiator = 1
token_list = [initiator]
curr = initiator

print(f"Node {initiator} detected coordinator failure. Starting Ring Election.")
while True:
    nxt = ring[curr]["next"]
    while not ring[nxt]["active"]:
        nxt = ring[nxt]["next"]  # Skip dead nodes

    if nxt == initiator:
        print(f"Token message returned to initiator {initiator}: {token_list}")
        break

    token_list.append(nxt)
    print(
        f"Token message circulation across active ring nodes: {curr} -> {nxt} (List: {token_list})"
    )
    curr = nxt

# 4. Elect highest ID / priority and broadcast[cite: 4]
elected_leader = max(token_list)
print(f"\n[ELECTED] Node {elected_leader} with the highest ID is elected Leader.")
for nid in token_list:
    if nid != elected_leader:
        print(f"Elected Leader {elected_leader} notifying Node {nid}")

##rmi

import csv
import json

# 1. Create the CSV file
csv_data = """call_id,client_name,method_name,param_value,timestamp
101,Client_A,processData,450,10:00:01
102,Client_B,processData,1200,10:00:05
"""
with open("rpc_calls_1.csv", "w") as f:
    f.write(csv_data.strip())


# 2. Remote Procedures (TrustMesh Server)
def processData(val):
    val = float(val)
    status = "VALID" if val < 1000 else "ANOMALY"
    return {"status": status, "metric": val, "block": "0xABC123"}


# 3. Read CSV and Dispatch Calls
with open("rpc_calls_1.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # [DISPATCH] Marshal call to JSON
        marshaled_request = json.dumps(
            {"method": row["method_name"], "param": row["param_value"]}
        )
        print(f"[DISPATCH] Client invoking method -> {marshaled_request}")

        # [SERVER EXECUTION] Unmarshal and execute
        req = json.loads(marshaled_request)
        print(f"[SERVER EXECUTION] Processing parameter -> {req['param']}")

        if req["method"] == "processData":
            result = processData(req["param"])

        # [RETURN] Marshal back and print
        returned_payload = json.dumps(result)
        print(f"[RETURN] Result printed to terminal -> {returned_payload}\n")

##vector

import csv

# 1. Setup Dataset[cite: 2]
with open("vector_events_6.csv", "w") as f:
    f.write(
        "event_id,process_id,event_action,target_process\n"
        "E1,P1,INTERNAL,\n"
        "E2,P1,SEND,P2\n"
        "E3,P2,RECV,P1\n"
        "E4,P3,INTERNAL,\n"
    )

# 2. Vector Clock Tracking[cite: 2]
p_idx = {"P1": 0, "P2": 1, "P3": 2}
vc = {"P1": [0, 0, 0], "P2": [0, 0, 0], "P3": [0, 0, 0]}
event_vectors = {}
sent_vector = None

with open("vector_events_6.csv", "r") as f:
    for row in csv.DictReader(f):
        eid = row["event_id"]
        pid = row["process_id"]
        action = row["event_action"].strip().upper()
        idx = p_idx[pid]

        vc[pid][idx] += 1
        if action == "SEND":
            sent_vector = list(vc[pid])
        elif action == "RECV" and sent_vector:
            for i in range(3):
                vc[pid][i] = max(vc[pid][i], sent_vector[i])

        event_vectors[eid] = list(vc[pid])
        print(f"Event {eid} ({pid} {action}): Updated vector clock -> {vc[pid]}")  #[cite: 2]


# 3. Determine Causal Precedence vs Concurrency[cite: 2]
def compare_vectors(v1, v2):
    less_equal = all(x <= y for x, y in zip(v1, v2))
    strictly_less = less_equal and any(x < y for x, y in zip(v1, v2))
    greater_equal = all(x >= y for x, y in zip(v1, v2))
    strictly_greater = greater_equal and any(x > y for x, y in zip(v1, v2))

    if strictly_less:
        return "Causally Preceding (V1 < V2)"  #[cite: 2]
    elif strictly_greater:
        return "Causally Succeeding (V1 > V2)"
    else:
        return "Concurrent (E1 || E2)"  #[cite: 2]


print("\n--- Causality Checks ---")
print(
    f"E1 {event_vectors['E1']} vs E3 {event_vectors['E3']}: {compare_vectors(event_vectors['E1'], event_vectors['E3'])}"
)
print(
    f"E3 {event_vectors['E3']} vs E4 {event_vectors['E4']}: {compare_vectors(event_vectors['E3'], event_vectors['E4'])}"
)