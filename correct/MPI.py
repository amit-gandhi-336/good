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