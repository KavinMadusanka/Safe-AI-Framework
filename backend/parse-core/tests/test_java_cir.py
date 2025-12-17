import requests, json # type: ignore

FILE_PATH = r"D:\SLIIT\Year 4\RP\PROJECT\CIRDemo.java"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

payload = {"code": code, "filename": "CIRDemo.java"}

resp = requests.post("http://127.0.0.1:7070/parse", json=payload)
print(json.dumps(resp.json(), indent=2))
