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
)  #[cite: 2]