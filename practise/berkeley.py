import csv

with open("node_clocks_3.csv", "w") as f:
    f.write(
        "node_id,clock_time_sec,is_faulty\n"
        "N1,3600,FALSE\n"
        "N2,3605,FALSE\n"
        "N3,3595,FALSE\n"
        "N4,4200,TRUE\n"  # Outlier/faulty[cite: 1]
    )

