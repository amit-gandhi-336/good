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