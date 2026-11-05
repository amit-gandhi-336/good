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