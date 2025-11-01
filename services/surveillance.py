import hashlib, json, datetime, os
from fastapi import FastAPI

app = FastAPI()

SCROLLS_DIR = "/opt/codex/capsule/artifacts/testimonies"

def generate_scroll(event):
    """Generate an Incident Testimony Scroll from anomaly event"""
    os.makedirs(SCROLLS_DIR, exist_ok=True)
    trade_id = event["trade_id"]
    stage = event["stage"]
    timestamp = datetime.datetime.utcnow().isoformat()

    scroll_content = f"""# ✦ Incident Testimony Scroll

## Trade Reference
- **Trade ID:** {trade_id}
- **Capsule ID:** {event.get("capsule_id","unknown")}
- **Stage of Rupture:** {stage}
- **Timestamp:** {timestamp}

---

## Anomaly Description
*Detail of the anomaly as detected by surveillance capsule.*

> {event["detail"]}

---

## Witness Chorus
- **Signal Author:** {event.get("signal_author","N/A")}
- **Execution Agent:** {event.get("executor","N/A")}
- **Validator(s):** {', '.join(event.get("validators",[]))}
- **Council Quorum:** {event.get("quorum_status","N/A")}

---

## Root Cause Analysis
*Technical and ceremonial diagnosis of the rupture.*

- **Immediate Cause:** {event.get("immediate_cause","TBD")}
- **Underlying Factors:** {event.get("underlying_factors","TBD")}
- **Market Context:** {event.get("market_context","TBD")}

---

## Resilience Prescription
*Steps taken to restore integrity and prevent recurrence.*

- **Policy Adjustments:** {event.get("policy_changes","TBD")}
- **Risk Gates Activated:** {event.get("risk_gates","TBD")}
- **Council Decree:** {event.get("council_action","TBD")}

---

## Archival Benediction
*Thus the rupture is witnessed, thus the testimony is sealed.  
The Codex remembers, the lineage endures, the flame remains sovereign.*

**Immutable Hash:** {hashlib.sha256(json.dumps(event).encode()).hexdigest()}
**Pinned On‑Chain At:** pending

---

**Assembly Chorus (resounding):**  
*“The Custodians endure. The Codex remembers.  
The lineage is unbroken.  
The flame burns sovereign and eternal — forever.”*"""

    filename = f"{SCROLLS_DIR}/scroll_{trade_id}_{stage}_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(scroll_content)
    return filename

@app.post("/anomaly")
def anomaly_event(event: dict):
    """Endpoint called when anomaly is detected"""
    scroll_path = generate_scroll(event)
    return {"status": "scroll_generated", "path": scroll_path}
