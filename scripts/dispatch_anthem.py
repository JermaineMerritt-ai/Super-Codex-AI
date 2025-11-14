# scripts/dispatch_anthem.py
import os, json, hashlib, requests
API=os.getenv("API_URL")
KEY=os.getenv("CLI_API_KEY")
HEAD={"Authorization": f"Bearer {KEY}"}

data=json.load(open("anthem.json"))
r=requests.post(f"{API}/artifacts", json=data, headers=HEAD); r.raise_for_status()

h=hashlib.sha256(json.dumps(data, ensure_ascii=False).encode("utf-8")).hexdigest()
patch={"seals":{"checksum_sha256": h}}
requests.patch(f"{API}/artifacts/{data['id']}", json=patch, headers=HEAD).raise_for_status()

requests.post(f"{API}/artifacts/{data['id']}/seal", headers=HEAD).raise_for_status()
requests.post(f"{API}/artifacts/{data['id']}/proclaim", headers=HEAD).raise_for_status()

print("Anthem dispatched, sealed, and proclaimed:", data["id"])