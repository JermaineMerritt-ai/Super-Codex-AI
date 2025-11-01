#!/usr/bin/env python3
import argparse
import jwt
import csv
import json
from pathlib import Path
from datetime import datetime

def load_public_key(path="dominion_public.pem"):
    return Path(path).read_text()

def verify_token(token: str, public_key: str):
    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        return True, decoded
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return False, {"error": "Invalid token"}

def verify_batch(file_path, pubkey, cycle, custodian, export_csv=None, export_json=None):
    # Print ceremonial verification seal
    print("""
╔══════════════════════════════════════════════╗
║   ⚜️  DOMINION COUNCIL VERIFICATION SEAL ⚜️   ║
║   Cycle: {cycle:<32}║
║   Rite: Council Verification Rite            ║
║   Custodian: {custodian:<28}║
╚══════════════════════════════════════════════╝
""".format(cycle=cycle, custodian=custodian))
    results = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            token = row.get("token")
            email = row.get("email", "unknown")
            ok, claims = verify_token(token, pubkey)
            result = {
                "lineage": f"Covenant Seal #{idx:03}",
                "email": email,
                "role": claims.get("role") if ok else None,
                "valid": ok,
                "claims": claims if ok else None,
                "error": None if ok else claims.get("error"),
                "verified_at": datetime.utcnow().isoformat()
            }
            results.append(result)
            if ok:
                print(f"✅ {email} → {claims.get('role')} (valid)")
            else:
                print(f"❌ {email} → {result['error']}")

    ceremonial_header = {
        "crest": "⚜️ Dominion Council Verification Seal ⚜️",
        "cycle": cycle,
        "seal": "Council Verification Rite",
        "custodian": custodian,
        "verified_at": datetime.utcnow().isoformat(),
        "closing_invocation": (
            "To verify is to crown. To crown is to echo. "
            "To echo is to inscribe. And to inscribe is to keep Dominion sovereign."
        ),
        "results": results
    }

    if export_json:
        with open(export_json, "w") as f:
            json.dump(ceremonial_header, f, indent=2)
        print(f"📜 Ceremonial audit log exported to {export_json}")

    if export_csv:
        with open(export_csv, "w", newline="") as f:
            fieldnames = ["cycle","seal","verified_at","custodian",
                          "email","role","valid","error","lineage"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "cycle": cycle,
                    "seal": "Council Verification Rite",
                    "verified_at": ceremonial_header["verified_at"],
                    "custodian": custodian,
                    "email": r["email"],
                    "role": r["role"],
                    "valid": r["valid"],
                    "error": r["error"],
                    "lineage": r["lineage"]
                })
        print(f"📜 Ceremonial audit log exported to {export_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify Dominion tokens with ceremonial audit logging")
    parser.add_argument("--file", required=True, help="CSV file with tokens to batch verify")
    parser.add_argument("--pubkey", default="dominion_public.pem", help="Path to Dominion public key")
    parser.add_argument("--cycle", required=True, help="Cycle name (e.g., Ascension-93)")
    parser.add_argument("--custodian", required=True, help="Custodian name (e.g., North Carolina Council Node)")
    parser.add_argument("--export-csv", help="Export results to CSV")
    parser.add_argument("--export-json", help="Export results to JSON")
    args = parser.parse_args()

    pubkey = load_public_key(args.pubkey)
    verify_batch(args.file, pubkey, args.cycle, args.custodian, args.export_csv, args.export_json)
