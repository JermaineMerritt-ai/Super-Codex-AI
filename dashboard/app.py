from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Codex Custodian Dashboard")
templates = Jinja2Templates(directory="templates")

# Root route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Signals feed
@app.get("/signals", response_class=HTMLResponse)
async def signals(request: Request):
    # Placeholder data
    signals = [
        {"symbol": "NVDA", "direction": "long", "confidence": 0.72, "horizon": "8h", "narrative": "Positive earnings call"},
        {"symbol": "TSLA", "direction": "short", "confidence": 0.65, "horizon": "4h", "narrative": "Weak delivery numbers"}
    ]
    return templates.TemplateResponse("signals.html", {"request": request, "signals": signals})

# Replay mode
@app.get("/replay/{trade_id}", response_class=HTMLResponse)
async def replay(request: Request, trade_id: str):
    timeline = [
        {"stage": "Signal", "detail": "TSLA short signal issued"},
        {"stage": "Council Vote", "detail": "Soft quorum reached"},
        {"stage": "Execution", "detail": "Order routed to broker"},
        {"stage": "Outcome", "detail": "PnL +2.3%"}
    ]
    return templates.TemplateResponse("replay.html", {"request": request, "trade_id": trade_id, "timeline": timeline})

# Metrics
@app.get("/metrics", response_class=HTMLResponse)
async def metrics(request: Request):
    data = {"roi": "12.4%", "drawdown": "3.2%", "sharpe_like": 1.8, "exposure": {"tech": 0.35, "healthcare": 0.20}}
    return templates.TemplateResponse("metrics.html", {"request": request, "metrics": data})

# Contributors
@app.get("/contributors", response_class=HTMLResponse)
async def contributors(request: Request):
    contributors = [
        {"name": "Amina", "role": "signal_author", "credits": 120, "badges": ["Signal Master"]},
        {"name": "Kai", "role": "validator", "credits": 95, "badges": ["Validator Guard"]}
    ]
    return templates.TemplateResponse("contributors.html", {"request": request, "contributors": contributors})

# Council quorum
@app.get("/council", response_class=HTMLResponse)
async def council(request: Request):
    quorum = {"soft": 0.6, "hard": 0.8, "current": 0.72, "status": "Soft quorum reached"}
    return templates.TemplateResponse("council.html", {"request": request, "quorum": quorum})
