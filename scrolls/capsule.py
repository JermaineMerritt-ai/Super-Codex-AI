# scrolls/capsule.py
from fastapi import APIRouter
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from engines.rag import RAGEngine
from engines.axiom import AXIOM
from engines.sigil import SIGIL
from engines.oracle import ORACLE
from engines.lantern import LANTERN
from engines.flame import FLAME

router = APIRouter(prefix="/scrolls", tags=["scrolls"])
env = Environment(loader=FileSystemLoader("scrolls/templates"), autoescape=select_autoescape(["html"]))

rag = RAGEngine(); rag.load()
axiom = AXIOM(); sigil = SIGIL(); oracle = ORACLE(); lantern = LANTERN(); flame = FLAME()

class ResumePayload(BaseModel):
    name: str
    roles: list[str]
    highlights_query: str

@router.post("/resume")
def resume_scroll(payload: ResumePayload):
    sig = sigil.crown(payload.name, payload.roles)
    docs = rag.retrieve(payload.highlights_query, top_k=5)
    highlights = [d.page_content[:240] for d in docs]
    html = env.get_template("resume_scroll.jinja").render(
        name=payload.name, roles=payload.roles, highlights=highlights
    )
    axiom.audit("scroll_resume_dispatch", {"name": payload.name, "roles": payload.roles})
    flame.dispatch("resume", {"html": html, "identity": sig})
    return {"html": html, "identity": sig}

class FinancePayload(BaseModel):
    budget_series: list[float]
    tools: list[str]
    augment_query: str | None = None

@router.post("/finance")
def finance_scroll(payload: FinancePayload):
    foresight = oracle.foresight(payload.budget_series, horizon=6)
    augment = []
    if payload.augment_query:
        augment = [d.page_content[:240] for d in rag.retrieve(payload.augment_query, top_k=4)]
    tools = payload.tools + [f"forecast:{round(v,2)}" for v in foresight["forecast"]]
    html = env.get_template("finance_scroll.jinja").render(budget=str(payload.budget_series[-1]), grants=str(foresight["trend"]), tools=tools + augment)
    axiom.audit("scroll_finance_dispatch", {"trend": foresight["trend"], "last_budget": payload.budget_series[-1]})
    flame.dispatch("finance", {"html": html, "foresight": foresight})
    return {"html": html, "foresight": foresight}

class GovernancePayload(BaseModel):
    protocols: list[str]
    augment_query: str
    role: str

@router.post("/governance101")
def governance_scroll(payload: GovernancePayload):
    steps = lantern.onboarding_steps(payload.role)
    docs = rag.retrieve(payload.augment_query, top_k=6)
    protocols = payload.protocols + [d.page_content.split("\n")[0][:120] for d in docs] + steps
    html = env.get_template("governance101_scroll.jinja").render(protocols=protocols)
    axiom.audit("scroll_governance_dispatch", {"count": len(protocols), "role": payload.role})
    flame.dispatch("governance101", {"html": html, "protocols": protocols})
    return {"html": html, "protocols": protocols}