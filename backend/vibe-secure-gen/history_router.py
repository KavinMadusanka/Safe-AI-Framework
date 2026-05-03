# backend/vibe-secure-gen/history_router.py
"""
History API router.

HOW TO MOUNT — add these 2 lines to main.py:

    from history_router import router as history_router
    app.include_router(history_router, prefix="/api")

Endpoints:
    GET    /api/history          -> list all entries (newest first)
    POST   /api/history/save     -> add one entry
    DELETE /api/history/{id}     -> delete one entry
    DELETE /api/history          -> delete ALL entries
"""

import json
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router       = APIRouter()
HISTORY_FILE = Path(__file__).parent / "history.json"
_LOCK        = threading.Lock()
MAX_ENTRIES  = 100


# ── Pydantic sub-models ───────────────────────────────────────────────────────

class FixSummary(BaseModel):
    initial_issues:   Optional[int]   = None
    semgrep_fixed:    Optional[int]   = None
    llm_fixed:        Optional[int]   = None
    remaining_issues: Optional[int]   = None
    fix_rate_percent: Optional[float] = None
    dast_findings:    Optional[int]   = None
    dast_fixed:       Optional[int]   = None
    dast_remaining:   Optional[int]   = None


class UmlDiagramStore(BaseModel):
    class_svg:        Optional[str] = None
    package_svg:      Optional[str] = None
    sequence_svg:     Optional[str] = None
    component_svg:    Optional[str] = None
    activity_svg:     Optional[str] = None
    ai_class_svg:     Optional[str] = None
    ai_package_svg:   Optional[str] = None
    ai_sequence_svg:  Optional[str] = None
    ai_component_svg: Optional[str] = None
    ai_activity_svg:  Optional[str] = None


# ── NEW: SAST report snapshot ─────────────────────────────────────────────────

class SastFinding(BaseModel):
    check_id:    Optional[str]  = None
    severity:    Optional[str]  = None
    message:     Optional[str]  = None
    path:        Optional[str]  = None
    start:       Optional[Dict[str, Any]] = None
    has_autofix: Optional[bool] = None


class SastCategorizedFindings(BaseModel):
    initially_auto_fixable: Optional[List[SastFinding]] = None
    initially_manual_only:  Optional[List[SastFinding]] = None


class SastReport(BaseModel):
    initial_findings:     Optional[int]                       = None
    semgrep_fixed:        Optional[int]                       = None
    llm_fixed:            Optional[int]                       = None
    remaining_issues:     Optional[int]                       = None
    fix_rate_percent:     Optional[float]                     = None
    packs:                Optional[List[str]]                 = None
    languages:            Optional[List[str]]                 = None
    categorized_findings: Optional[SastCategorizedFindings]  = None


# ── NEW: DAST report snapshot ─────────────────────────────────────────────────

class DastFindingSnapshot(BaseModel):
    check_id:  str
    severity:  str
    message:   str
    owasp:     Optional[str]  = None
    cwe:       Optional[str]  = None
    line:      Optional[int]  = None
    file:      Optional[str]  = None
    fix_hint:  Optional[str]  = None
    source:    Optional[str]  = None


class DastReport(BaseModel):
    ok:               Optional[bool]                     = None
    docker_available: Optional[bool]                     = None
    total:            Optional[int]                      = None
    critical:         Optional[int]                      = None
    high:             Optional[int]                      = None
    medium:           Optional[int]                      = None
    low:              Optional[int]                      = None
    owasp_coverage:   Optional[List[str]]                = None
    pattern_count:    Optional[int]                      = None
    runtime_count:    Optional[int]                      = None
    languages:        Optional[List[str]]                = None
    llm_fixed:        Optional[int]                      = None
    llm_fix_applied:  Optional[bool]                     = None
    findings:         Optional[List[DastFindingSnapshot]] = None


# ── Main history entry model ──────────────────────────────────────────────────

class HistoryEntry(BaseModel):
    id:            str
    timestamp:     str
    prompt:        str
    code:          str
    original_code: Optional[str]          = None
    fix_summary:   Optional[FixSummary]   = None
    languages:     Optional[List[str]]    = None
    decision:      Optional[str]          = None
    uml:           Optional[UmlDiagramStore] = None
    # ── NEW fields — security report snapshots ────────────────────────────
    sast_report:   Optional[SastReport]   = None
    dast_report:   Optional[DastReport]   = None


# ── Storage helpers ───────────────────────────────────────────────────────────

def _load() -> List[Dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(entries: List[Dict[str, Any]]) -> None:
    HISTORY_FILE.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/history")
def get_history():
    with _LOCK:
        entries = _load()
    return {"history": entries, "count": len(entries)}


@router.post("/history/save", status_code=201)
def save_history(entry: HistoryEntry):
    with _LOCK:
        entries = _load()
        # Use model_dump (Pydantic v2) with fallback to dict() for Pydantic v1
        try:
            entry_dict = entry.model_dump()
        except AttributeError:
            entry_dict = entry.dict()
        entries.insert(0, entry_dict)
        entries = entries[:MAX_ENTRIES]
        _save(entries)
    return {"ok": True, "id": entry.id}


@router.delete("/history/{entry_id}")
def delete_entry(entry_id: str):
    with _LOCK:
        entries = _load()
        before  = len(entries)
        entries = [e for e in entries if e.get("id") != entry_id]
        if len(entries) == before:
            raise HTTPException(status_code=404, detail="Entry not found")
        _save(entries)
    return {"ok": True, "deleted": entry_id}


@router.delete("/history")
def clear_history():
    with _LOCK:
        _save([])
    return {"ok": True}