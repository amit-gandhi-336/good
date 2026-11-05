import csv
import json

csv_data= """call_id,client_name,method_name,param_value,timestamp
101,Client_A,processData,450,10:00:01
102,Client_B,processData,1200,10:00:05
"""

with open("rpc_calls_1.csv","w") as f:
    f.write(csv_data.strip())

def processData(val):
    val=float(val)
    status="VALID" if val<1000 else "ANOMALY"
    return {"status":status,"metric":val,"block":"0xABC123"}

with open("rpc_calls_1.csv","r") as f:
    reader=csv.DictReader(f)
    for row in reader:
        marshaled_request = json.dumps({"method":row["method_name"],"param":row["param_value"]})
        print(f"[DISPATCH] Client invoking method -> {marshaled_request}")
        
        req=json.loads(marshaled_request)
        print(f"[SERVER EXECUTION] Processing parameter -> {req['param']}")
        if req["method"]=="processData":
            result=processData(req["param"])

        returned_payload=json.dumps(result)
        print(f"[RETURN] Result printed to terminal -> {returned_payload}\n")