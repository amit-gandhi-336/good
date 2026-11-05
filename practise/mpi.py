import csv 
from concurrent.futures import ThreadPoolExecutor

with open("matrix_22.csv", "w") as f:
    f.write(
        "row_id,col_0,col_1,col_2,col_3\n"
        "R0,2,4,1,5\n"
        "R1,1,3,0,2\n"
        "R2,3,1,2,4\n"
        "R3,0,2,5,1\n"
    )

B=[1,2,3,4]

def worker_dot_product(task):
    row_id,row_vals=task
    res = sum(x*y for x,y in zip(row_vals,B))
    print(f"[WORKER] Computed partial dot product for {row_id} = {res}")
    return row_id,res

A=[]
with open("matrix_22.csv","r") as f:
    for row in csv.DictReader(f):
        r_vals=[int(row["col_0"]),int(row["col_1"]),int(row["col_2"]),int(row["col_3"])]
        A.append((row["row_id"],r_vals))

print(f"[MASTER] Scattering {len(A)} matrix rows to worker tasks...")

final_product={}

with ThreadPoolExecutor(max_workers=4) as executor:
    results=executor.map(worker_dot_product,A)
    for r_id,dot in results:
        final_product[r_id]=dot
print("\n[MASTER GATHER] Final matrix product result vector:")  #[cite: 4]
for r_id in sorted(final_product.keys()):
    print(f"  {r_id}: {final_product[r_id]}")