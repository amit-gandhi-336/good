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