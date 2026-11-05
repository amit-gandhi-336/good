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