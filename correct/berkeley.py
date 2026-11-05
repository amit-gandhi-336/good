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