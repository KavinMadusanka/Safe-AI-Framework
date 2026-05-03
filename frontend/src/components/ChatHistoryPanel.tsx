// frontend/src/components/ChatHistoryPanel.tsx

import { useEffect, useState } from "react";
import {
  X, Clock, Shield, ChevronRight,
  Trash2, Search, CheckCircle2, RotateCcw,
  AlertTriangle, Activity, ChevronDown,
} from "lucide-react";

/* ── Exported type (used in SecureGenerator.tsx too) ─────────────────────── */
export type HistoryEntry = {
  id:             string;
  timestamp:      string;
  prompt:         string;
  code:           string;
  original_code?: string;
  fix_summary?: {
    initial_issues?:   number;
    semgrep_fixed?:    number;
    llm_fixed?:        number;
    remaining_issues?: number;
    fix_rate_percent?: number;
  };
  languages?: string[];
  decision?:  string;
  uml?: {
    class_svg?:             string | null;
    package_svg?:           string | null;
    sequence_svg?:          string | null;
    component_svg?:         string | null;
    activity_svg?:          string | null;
    ai_class_svg?:          string | null;
    ai_package_svg?:        string | null;
    ai_sequence_svg?:       string | null;
    ai_component_svg?:      string | null;
    ai_activity_svg?:       string | null;
  };
  // ── NEW: Full security report data ────────────────────────────────────
  sast_report?: {
    initial_findings?:   number;
    semgrep_fixed?:      number;
    llm_fixed?:          number;
    remaining_issues?:   number;
    fix_rate_percent?:   number;
    packs?:              string[];
    languages?:          string[];
    categorized_findings?: {
      initially_auto_fixable?: Array<{
        check_id?: string;
        severity?: string;
        message?:  string;
        path?:     string;
        start?:    { line?: number };
        has_autofix?: boolean;
      }>;
      initially_manual_only?: Array<{
        check_id?: string;
        severity?: string;
        message?:  string;
        path?:     string;
        start?:    { line?: number };
        has_autofix?: boolean;
      }>;
    };
  };
  dast_report?: {
    ok?:              boolean;
    docker_available?: boolean;
    total?:           number;
    critical?:        number;
    high?:            number;
    medium?:          number;
    low?:             number;
    owasp_coverage?:  string[];
    pattern_count?:   number;
    runtime_count?:   number;
    languages?:       string[];
    llm_fixed?:       number;
    llm_fix_applied?: boolean;
    findings?: Array<{
      check_id:  string;
      severity:  string;
      message:   string;
      owasp?:    string;
      cwe?:      string | null;
      line?:     number | null;
      file?:     string | null;
      fix_hint?: string | null;
      source?:   string;
    }>;
  };
};

type Props = {
  open:      boolean;
  onClose:   () => void;
  onRestore: (entry: HistoryEntry) => void;
};

/* ── Constants ───────────────────────────────────────────────────────────── */
const API_HISTORY = "http://localhost:8000/api/history";
const LS_KEY      = "secure_gen_history";

/* ── Small helpers ───────────────────────────────────────────────────────── */
function formatTime(ts: string): string {
  try {
    const d    = new Date(ts);
    const diff = Date.now() - d.getTime();
    const mins = Math.floor(diff / 60_000);
    const hrs  = Math.floor(diff / 3_600_000);
    const days = Math.floor(diff / 86_400_000);
    if (mins <  1) return "Just now";
    if (mins < 60) return `${mins}m ago`;
    if (hrs  < 24) return `${hrs}h ago`;
    if (days <  7) return `${days}d ago`;
    return d.toLocaleDateString();
  } catch {
    return ts;
  }
}

function statusColor(entry: HistoryEntry): string {
  const r = entry.fix_summary?.fix_rate_percent ?? 100;
  if (r >= 100) return "#10b981";
  if (r >=  70) return "#f59e0b";
  return "#ef4444";
}

const SEV_COLOR: Record<string, string> = {
  CRITICAL: "#ef4444",
  HIGH:     "#f97316",
  MEDIUM:   "#f59e0b",
  LOW:      "#3b82f6",
  INFO:     "#94a3b8",
  ERROR:    "#ef4444",
  WARNING:  "#f59e0b",
};
const SEV_BG: Record<string, string> = {
  CRITICAL: "rgba(239,68,68,0.1)",
  HIGH:     "rgba(249,115,22,0.1)",
  MEDIUM:   "rgba(245,158,11,0.1)",
  LOW:      "rgba(59,130,246,0.1)",
  INFO:     "rgba(148,163,184,0.1)",
  ERROR:    "rgba(239,68,68,0.1)",
  WARNING:  "rgba(245,158,11,0.1)",
};

/* ── SAST Section ────────────────────────────────────────────────────────── */
function SastSection({ sast }: { sast: HistoryEntry["sast_report"] }) {
  const [open, setOpen] = useState(false);
  if (!sast) return null;

  const initial   = sast.initial_findings ?? 0;
  const semFixed  = sast.semgrep_fixed ?? 0;
  const llmFixed  = sast.llm_fixed ?? 0;
  const remaining = sast.remaining_issues ?? 0;
  const rate      = sast.fix_rate_percent ?? (initial === 0 ? 100 : 0);

  const allFindings = [
    ...(sast.categorized_findings?.initially_auto_fixable ?? []),
    ...(sast.categorized_findings?.initially_manual_only ?? []),
  ];

  return (
    <div style={{ marginBottom: 10 }}>
      {/* Header */}
      <div style={{
        display: "flex", alignItems: "center", gap: 6, marginBottom: 8,
        fontSize: 10, fontWeight: 700, color: "#8b5cf6",
        textTransform: "uppercase", letterSpacing: "0.08em",
      }}>
        <Shield size={11} color="#8b5cf6" />
        SAST Auto-Fix Results
      </div>

      {initial === 0 ? (
        <div style={{
          padding: "8px 12px", borderRadius: 7,
          background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)",
          display: "flex", alignItems: "center", gap: 6,
          fontSize: 11, color: "#10b981", fontWeight: 500,
        }}>
          <CheckCircle2 size={12} /> No SAST vulnerabilities found
        </div>
      ) : (
        <>
          {/* Stat grid */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 6, marginBottom: 8 }}>
            {[
              { label: "Initial",  val: initial,   color: "#ef4444" },
              { label: "Semgrep",  val: semFixed,  color: "#10b981" },
              { label: "LLM",      val: llmFixed,  color: "#60a5fa" },
              { label: "Left",     val: remaining, color: remaining === 0 ? "#10b981" : "#f59e0b" },
            ].map(({ label, val, color }) => (
              <div key={label} style={{
                padding: "7px 6px", background: "#080611",
                borderRadius: 6, border: "1px solid #1e1b2e", textAlign: "center",
              }}>
                <div style={{ fontSize: 16, fontWeight: 700, color, lineHeight: 1 }}>{val}</div>
                <div style={{ fontSize: 9, color: "#475569", marginTop: 3 }}>{label}</div>
              </div>
            ))}
          </div>

          {/* Progress bar */}
          <div style={{ marginBottom: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4, fontSize: 10 }}>
              <span style={{ color: "#475569" }}>Fix rate</span>
              <span style={{ color: "#10b981", fontWeight: 700 }}>{rate.toFixed(0)}%</span>
            </div>
            <div style={{ width: "100%", height: 5, background: "#1e1530", borderRadius: 999, overflow: "hidden" }}>
              <div style={{
                width: `${rate}%`, height: "100%",
                background: "linear-gradient(90deg,#7c3aed,#10b981)",
                borderRadius: 999,
              }} />
            </div>
          </div>

          {/* Collapsible findings list */}
          {allFindings.length > 0 && (
            <>
              <button
                onClick={() => setOpen(!open)}
                style={{
                  width: "100%", padding: "7px 10px", borderRadius: 6,
                  background: open ? "#1a1130" : "#0f0d1a",
                  border: `1px solid ${open ? "#7c3aed" : "#1e1b2e"}`,
                  color: "#94a3b8", fontSize: 11, fontWeight: 600,
                  cursor: "pointer", display: "flex", alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <span>{allFindings.length} vulnerability{allFindings.length !== 1 ? "ies" : "y"} detected</span>
                <ChevronDown size={12} color="#475569" style={{ transform: open ? "rotate(180deg)" : "none", transition: "transform .2s" }} />
              </button>

              {open && (
                <div style={{ marginTop: 6, display: "flex", flexDirection: "column", gap: 4, maxHeight: 220, overflowY: "auto" }}>
                  {allFindings.map((f, i) => {
                    const sev   = (f.severity ?? "INFO").toUpperCase();
                    const color = SEV_COLOR[sev] ?? "#94a3b8";
                    const bg    = SEV_BG[sev]    ?? "rgba(148,163,184,0.1)";
                    return (
                      <div key={i} style={{
                        padding: "8px 10px", borderRadius: 6,
                        background: "#080611", border: `1px solid ${color}25`,
                      }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
                          <span style={{
                            fontSize: 8, fontWeight: 700, padding: "1px 5px", borderRadius: 3,
                            color, background: bg, textTransform: "uppercase",
                          }}>{sev}</span>
                          <span style={{ fontSize: 9, color: "#475569", fontFamily: "monospace" }}>
                            {f.check_id ?? "unknown"}
                          </span>
                          {f.has_autofix && (
                            <span style={{ marginLeft: "auto", fontSize: 8, color: "#10b981", fontWeight: 600 }}>
                              ✔ auto-fixed
                            </span>
                          )}
                        </div>
                        <div style={{ fontSize: 10, color: "#94a3b8", lineHeight: 1.4 }}>
                          {f.message ?? "No description"}
                        </div>
                        {f.path && (
                          <div style={{ fontSize: 9, color, fontFamily: "monospace", marginTop: 3 }}>
                            {f.path}{f.start?.line ? `:${f.start.line}` : ""}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  );
}

/* ── DAST Section ────────────────────────────────────────────────────────── */
function DastSection({ dast }: { dast: HistoryEntry["dast_report"] }) {
  const [open, setOpen] = useState(false);
  if (!dast) return null;

  const total     = dast.total ?? 0;
  const llmFixed  = dast.llm_fixed ?? 0;
  const remaining = total - llmFixed;

  return (
    <div>
      {/* Header */}
      <div style={{
        display: "flex", alignItems: "center", gap: 6, marginBottom: 8,
        fontSize: 10, fontWeight: 700, color: "#f59e0b",
        textTransform: "uppercase", letterSpacing: "0.08em",
      }}>
        <Activity size={11} color="#f59e0b" />
        Dynamic Analysis (DAST)
        <span style={{
          marginLeft: "auto", fontSize: 9, padding: "1px 6px", borderRadius: 3,
          background: dast.docker_available ? "rgba(16,185,129,0.12)" : "rgba(245,158,11,0.12)",
          color:      dast.docker_available ? "#10b981" : "#f59e0b",
          fontWeight: 600,
        }}>
          {dast.docker_available ? "🐳 Docker" : "⚡ Pattern"}
        </span>
      </div>

      {total === 0 ? (
        <div style={{
          padding: "8px 12px", borderRadius: 7,
          background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)",
          display: "flex", alignItems: "center", gap: 6,
          fontSize: 11, color: "#10b981", fontWeight: 500,
        }}>
          <CheckCircle2 size={12} /> No runtime vulnerabilities detected
        </div>
      ) : (
        <>
          {/* Severity counters */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 6, marginBottom: 8 }}>
            {(["critical", "high", "medium", "low"] as const).map((sev) => {
              const val   = (dast as Record<string, number | undefined>)[sev] ?? 0;
              const color = SEV_COLOR[sev.toUpperCase()] ?? "#94a3b8";
              return (
                <div key={sev} style={{
                  padding: "7px 6px", background: "#080611",
                  borderRadius: 6, border: `1px solid ${val > 0 ? color + "40" : "#1e1b2e"}`,
                  textAlign: "center",
                }}>
                  <div style={{ fontSize: 16, fontWeight: 700, color: val > 0 ? color : "#334155", lineHeight: 1 }}>{val}</div>
                  <div style={{ fontSize: 9, color: "#475569", marginTop: 3, textTransform: "uppercase" }}>{sev.slice(0, 4)}</div>
                </div>
              );
            })}
          </div>

          {/* LLM fix summary if any */}
          {dast.llm_fix_applied && llmFixed > 0 && (
            <div style={{
              padding: "7px 10px", borderRadius: 6, marginBottom: 8,
              background: "rgba(16,185,129,0.07)", border: "1px solid rgba(16,185,129,0.25)",
              display: "flex", alignItems: "center", gap: 6,
              fontSize: 10, color: "#10b981",
            }}>
              <CheckCircle2 size={11} />
              LLM fixed {llmFixed} of {total} · {remaining} remaining
            </div>
          )}

          {/* OWASP chips */}
          {(dast.owasp_coverage ?? []).length > 0 && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginBottom: 8 }}>
              {dast.owasp_coverage!.map((o) => {
                const tag = o.match(/^(A\d+)/)?.[1] ?? o.slice(0, 3);
                return (
                  <span key={o} style={{
                    fontSize: 9, padding: "2px 6px", borderRadius: 4, fontWeight: 700,
                    background: "rgba(239,68,68,0.1)", color: "#fca5a5",
                    border: "1px solid rgba(239,68,68,0.2)",
                  }}>{tag}</span>
                );
              })}
            </div>
          )}

          {/* Collapsible findings */}
          {(dast.findings ?? []).length > 0 && (
            <>
              <button
                onClick={() => setOpen(!open)}
                style={{
                  width: "100%", padding: "7px 10px", borderRadius: 6,
                  background: open ? "#1a1130" : "#0f0d1a",
                  border: `1px solid ${open ? "#f59e0b40" : "#1e1b2e"}`,
                  color: "#94a3b8", fontSize: 11, fontWeight: 600,
                  cursor: "pointer", display: "flex", alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <span style={{ display: "flex", alignItems: "center", gap: 5 }}>
                  <AlertTriangle size={11} color="#f59e0b" />
                  {dast.findings!.length} finding{dast.findings!.length !== 1 ? "s" : ""}
                </span>
                <ChevronDown size={12} color="#475569" style={{ transform: open ? "rotate(180deg)" : "none", transition: "transform .2s" }} />
              </button>

              {open && (
                <div style={{ marginTop: 6, display: "flex", flexDirection: "column", gap: 4, maxHeight: 220, overflowY: "auto" }}>
                  {dast.findings!.map((f, i) => {
                    const sev   = (f.severity ?? "LOW").toUpperCase();
                    const color = SEV_COLOR[sev] ?? "#94a3b8";
                    const bg    = SEV_BG[sev]    ?? "rgba(148,163,184,0.1)";
                    return (
                      <div key={i} style={{
                        padding: "8px 10px", borderRadius: 6,
                        background: "#080611", border: `1px solid ${color}25`,
                      }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
                          <span style={{
                            fontSize: 8, fontWeight: 700, padding: "1px 5px", borderRadius: 3,
                            color, background: bg, textTransform: "uppercase",
                          }}>{sev}</span>
                          <span style={{ fontSize: 9, color: "#475569", fontFamily: "monospace" }}>
                            {f.check_id}
                          </span>
                          {f.source === "docker_execution" && (
                            <span style={{ fontSize: 8, color: "#818cf8", fontWeight: 600 }}>🐳 runtime</span>
                          )}
                        </div>
                        <div style={{ fontSize: 10, color: "#94a3b8", lineHeight: 1.4 }}>
                          {f.message}
                        </div>
                        {f.owasp && (
                          <div style={{ fontSize: 9, color: "#f97316", marginTop: 3, fontWeight: 600 }}>
                            {f.owasp}
                          </div>
                        )}
                        {f.fix_hint && (
                          <div style={{
                            marginTop: 5, padding: "5px 8px", borderRadius: 4,
                            background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.15)",
                            fontSize: 9, color: "#6ee7b7", lineHeight: 1.4,
                          }}>
                            {f.fix_hint}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          )}

          {/* Footer stats */}
          <div style={{
            marginTop: 8, padding: "6px 10px", borderRadius: 6,
            background: "#080611", border: "1px solid #1e1b2e",
            display: "flex", gap: 14, fontSize: 10, color: "#475569",
          }}>
            <span>Pattern: <span style={{ color: "#94a3b8", fontWeight: 600 }}>{dast.pattern_count ?? 0}</span></span>
            <span>Runtime: <span style={{ color: "#6366f1", fontWeight: 600 }}>{dast.runtime_count ?? 0}</span></span>
            {(dast.languages ?? []).length > 0 && (
              <span>Lang: <span style={{ color: "#94a3b8", fontWeight: 600 }}>{dast.languages!.join(", ")}</span></span>
            )}
          </div>
        </>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════════════ */
export default function ChatHistoryPanel({ open, onClose, onRestore }: Props) {
  const [entries,  setEntries]  = useState<HistoryEntry[]>([]);
  const [loading,  setLoading]  = useState(false);
  const [search,   setSearch]   = useState("");
  const [expanded, setExpanded] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  // Track which sub-tab is shown in expanded entry: "security" | "code"
  const [secTab, setSecTab] = useState<Record<string, "security" | "code">>({});

  useEffect(() => { if (open) fetchHistory(); }, [open]);

  async function fetchHistory() {
    setLoading(true);
    try {
      const res = await fetch(API_HISTORY);
      if (res.ok) {
        const data = await res.json();
        setEntries(data.history ?? []);
        setLoading(false);
        return;
      }
    } catch { /* fall through */ }
    try {
      const raw = localStorage.getItem(LS_KEY);
      setEntries(raw ? JSON.parse(raw) : []);
    } catch { setEntries([]); }
    setLoading(false);
  }

  async function deleteEntry(id: string, e: React.MouseEvent) {
    e.stopPropagation();
    setDeleting(id);
    try { await fetch(`${API_HISTORY}/${id}`, { method: "DELETE" }); } catch { /**/ }
    const updated = entries.filter((en) => en.id !== id);
    setEntries(updated);
    try { localStorage.setItem(LS_KEY, JSON.stringify(updated)); } catch { /**/ }
    setDeleting(null);
  }

  async function clearAll() {
    if (!confirm("Clear all generation history?")) return;
    try { await fetch(API_HISTORY, { method: "DELETE" }); } catch { /**/ }
    setEntries([]);
    try { localStorage.removeItem(LS_KEY); } catch { /**/ }
  }

  const filtered = entries.filter((e) =>
    e.prompt.toLowerCase().includes(search.toLowerCase())
  );

  if (!open) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: "fixed", inset: 0,
          background: "rgba(0,0,0,0.55)",
          zIndex: 200, backdropFilter: "blur(3px)",
        }}
      />

      {/* Slide-in panel — wider to fit security report */}
      <div
        style={{
          position: "fixed", top: 0, right: 0, bottom: 0, width: 480,
          background: "#13111e", borderLeft: "1px solid #2d2a3d",
          zIndex: 201, display: "flex", flexDirection: "column",
          animation: "hp-slide 0.25s cubic-bezier(0.16,1,0.3,1)",
        }}
      >
        <style>{`
          @keyframes hp-slide {
            from { transform: translateX(100%); opacity: 0; }
            to   { transform: translateX(0);    opacity: 1; }
          }
          .hp-row:hover  { background: #1a1730 !important; }
          .hp-row:hover .hp-del { opacity: 1 !important; }
          .hp-del { opacity: 0; transition: opacity .15s; }
          .sec-tab-btn { cursor: pointer; transition: all .15s; }
          .sec-tab-btn:hover { opacity: 0.85; }
        `}</style>

        {/* ── Header ── */}
        <div style={{
          padding: "18px 20px 16px", borderBottom: "1px solid #2d2a3d",
          background: "#1a1730", display: "flex", alignItems: "center",
          justifyContent: "space-between", flexShrink: 0,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{
              width: 34, height: 34, borderRadius: 9, flexShrink: 0,
              background: "linear-gradient(135deg,#6366f1,#8b5cf6)",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <Clock size={17} color="#fff" />
            </div>
            <div>
              <div style={{ fontSize: 15, fontWeight: 700, color: "#e2e8f0" }}>
                Generation History
              </div>
              <div style={{ fontSize: 11, color: "#64748b", marginTop: 1 }}>
                {entries.length} saved session{entries.length !== 1 ? "s" : ""}
              </div>
            </div>
          </div>

          <div style={{ display: "flex", gap: 8 }}>
            {entries.length > 0 && (
              <button onClick={clearAll} style={{
                padding: "6px 11px", borderRadius: 7, border: "1px solid #3d3a50",
                background: "transparent", color: "#ef4444", fontSize: 11,
                fontWeight: 600, cursor: "pointer", display: "flex", alignItems: "center", gap: 5,
              }}>
                <Trash2 size={12} /> Clear All
              </button>
            )}
            <button onClick={onClose} style={{
              width: 32, height: 32, borderRadius: 8, border: "1px solid #2d2a3d",
              background: "transparent", color: "#94a3b8", cursor: "pointer",
              display: "flex", alignItems: "center", justifyContent: "center", padding: 0,
            }}>
              <X size={16} />
            </button>
          </div>
        </div>

        {/* ── Search ── */}
        <div style={{ padding: "12px 16px", borderBottom: "1px solid #1e1b2e", flexShrink: 0 }}>
          <div style={{
            display: "flex", alignItems: "center", gap: 8,
            padding: "8px 13px", background: "#0f0d1a",
            borderRadius: 8, border: "1px solid #2d2a3d",
          }}>
            <Search size={13} color="#475569" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search history…"
              style={{ flex: 1, background: "none", border: "none", outline: "none", color: "#94a3b8", fontSize: 13 }}
            />
            {search && (
              <button onClick={() => setSearch("")}
                style={{ background: "none", border: "none", cursor: "pointer", padding: 0, color: "#475569" }}>
                <X size={13} />
              </button>
            )}
          </div>
        </div>

        {/* ── List ── */}
        <div style={{ flex: 1, overflowY: "auto" }}>
          {loading ? (
            <div style={{ padding: 48, textAlign: "center", color: "#475569", fontSize: 13 }}>
              Loading history…
            </div>
          ) : filtered.length === 0 ? (
            <div style={{ padding: 56, textAlign: "center" }}>
              <Clock size={36} color="#2d2a3d" style={{ display: "block", margin: "0 auto 14px" }} />
              <div style={{ fontSize: 14, fontWeight: 600, color: "#475569" }}>
                {search ? "No results found" : "No history yet"}
              </div>
              <div style={{ fontSize: 12, color: "#334155", marginTop: 5 }}>
                {search ? "Try a different search" : "Generated code will appear here"}
              </div>
            </div>
          ) : (
            filtered.map((entry) => {
              const isOpen    = expanded === entry.id;
              const sc        = statusColor(entry);
              const curTab    = secTab[entry.id] ?? "security";
              const hasSast   = !!entry.sast_report;
              const hasDast   = !!entry.dast_report;
              const hasReport = hasSast || hasDast;

              return (
                <div key={entry.id} style={{ borderBottom: "1px solid #1a1730" }}>

                  {/* Row */}
                  <div
                    className="hp-row"
                    onClick={() => setExpanded(isOpen ? null : entry.id)}
                    style={{
                      padding: "13px 16px", cursor: "pointer",
                      background: isOpen ? "#1a1730" : "transparent",
                      transition: "background .15s",
                      display: "flex", gap: 10, alignItems: "flex-start",
                    }}
                  >
                    <div style={{
                      width: 8, height: 8, borderRadius: "50%",
                      background: sc, boxShadow: `0 0 6px ${sc}70`,
                      marginTop: 5, flexShrink: 0,
                    }} />

                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{
                        fontSize: 13, fontWeight: 500, color: "#e2e8f0",
                        lineHeight: 1.4, whiteSpace: "nowrap",
                        overflow: "hidden", textOverflow: "ellipsis",
                      }}>
                        {entry.prompt}
                      </div>

                      <div style={{ display: "flex", gap: 8, marginTop: 5, alignItems: "center", flexWrap: "wrap" }}>
                        <span style={{ fontSize: 11, color: "#475569" }}>
                          {formatTime(entry.timestamp)}
                        </span>
                        {(entry.languages ?? []).length > 0 && (
                          <span style={{
                            fontSize: 10, color: "#8b5cf6",
                            background: "rgba(139,92,246,.12)",
                            padding: "2px 7px", borderRadius: 4,
                            fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em",
                          }}>
                            {entry.languages![0]}
                          </span>
                        )}
                        {(entry.fix_summary?.initial_issues ?? 0) > 0 && (
                          <span style={{ fontSize: 11, color: sc, display: "flex", alignItems: "center", gap: 3 }}>
                            <Shield size={10} />
                            {entry.fix_summary!.fix_rate_percent?.toFixed(0)}% fixed
                          </span>
                        )}
                        {(entry.fix_summary?.initial_issues ?? 0) === 0 && (
                          <span style={{ fontSize: 11, color: "#10b981", display: "flex", alignItems: "center", gap: 3 }}>
                            <CheckCircle2 size={10} /> Clean
                          </span>
                        )}
                        {/* DAST badge */}
                        {entry.dast_report && (entry.dast_report.total ?? 0) > 0 && (
                          <span style={{ fontSize: 11, color: "#f97316", display: "flex", alignItems: "center", gap: 3 }}>
                            <Activity size={10} />
                            {entry.dast_report.total} DAST
                          </span>
                        )}
                      </div>
                    </div>

                    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <button
                        className="hp-del"
                        onClick={(e) => deleteEntry(entry.id, e)}
                        disabled={deleting === entry.id}
                        title="Delete entry"
                        style={{
                          width: 26, height: 26, borderRadius: 6, border: "1px solid #2d2a3d",
                          background: "transparent", color: "#ef4444", cursor: "pointer",
                          display: "flex", alignItems: "center", justifyContent: "center", padding: 0,
                        }}
                      >
                        <Trash2 size={12} />
                      </button>
                      <ChevronRight
                        size={14} color="#475569"
                        style={{ transform: isOpen ? "rotate(90deg)" : "rotate(0)", transition: "transform .2s" }}
                      />
                    </div>
                  </div>

                  {/* Expanded section */}
                  {isOpen && (
                    <div style={{ background: "#0f0d1a", padding: "14px 16px 18px" }}>

                      {/* Sub-tab switcher — only show if we have security data */}
                      {hasReport && (
                        <div style={{
                          display: "flex", gap: 4, marginBottom: 14,
                          background: "#080611", borderRadius: 8, padding: 4,
                          border: "1px solid #1e1b2e",
                        }}>
                          {(["security", "code"] as const).map((tab) => (
                            <button
                              key={tab}
                              className="sec-tab-btn"
                              onClick={() => setSecTab((prev) => ({ ...prev, [entry.id]: tab }))}
                              style={{
                                flex: 1, padding: "6px", borderRadius: 6, border: "none",
                                background: curTab === tab
                                  ? tab === "security" ? "rgba(139,92,246,0.25)" : "rgba(79,12,135,0.2)"
                                  : "transparent",
                                color:   curTab === tab ? "#e2e8f0" : "#475569",
                                fontSize: 11, fontWeight: 600,
                                display: "flex", alignItems: "center", justifyContent: "center", gap: 5,
                              }}
                            >
                              {tab === "security" ? <><Shield size={11} /> Security Report</> : <><span style={{ fontSize: 11 }}>{"</>"}</span> Code Preview</>}
                            </button>
                          ))}
                        </div>
                      )}

                      {/* Security tab */}
                      {(!hasReport || curTab === "security") && hasReport && (
                        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                          <SastSection sast={entry.sast_report} />
                          {hasDast && <div style={{ height: 1, background: "#1e1b2e" }} />}
                          <DastSection dast={entry.dast_report} />
                        </div>
                      )}

                      {/* Code preview tab (or default if no report) */}
                      {(!hasReport || curTab === "code") && (
                        <>
                          {/* Stats row — shown only if no security tab OR we're on code tab */}
                          {(entry.fix_summary?.initial_issues ?? 0) > 0 && (
                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: 14 }}>
                              {[
                                { label: "Initial",   val: entry.fix_summary!.initial_issues,  color: "#ef4444" },
                                {
                                  label: "Fixed",
                                  val: (entry.fix_summary!.semgrep_fixed ?? 0) + (entry.fix_summary!.llm_fixed ?? 0),
                                  color: "#10b981",
                                },
                                {
                                  label: "Remaining",
                                  val:   entry.fix_summary!.remaining_issues,
                                  color: (entry.fix_summary!.remaining_issues ?? 0) === 0 ? "#10b981" : "#f59e0b",
                                },
                              ].map(({ label, val, color }) => (
                                <div key={label} style={{
                                  padding: "9px 10px", background: "#13111e",
                                  borderRadius: 8, border: "1px solid #2d2a3d", textAlign: "center",
                                }}>
                                  <div style={{ fontSize: 20, fontWeight: 700, color }}>{val}</div>
                                  <div style={{ fontSize: 10, color: "#475569", marginTop: 3 }}>{label}</div>
                                </div>
                              ))}
                            </div>
                          )}

                          <div style={{
                            fontSize: 10, color: "#475569", fontWeight: 600,
                            textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6,
                          }}>
                            Code Preview
                          </div>
                          <div style={{ position: "relative", marginBottom: 14 }}>
                            <pre style={{
                              margin: 0, padding: "10px 12px", background: "#0a0910",
                              borderRadius: 7, border: "1px solid #2d2a3d",
                              fontSize: 11, color: "#64748b", maxHeight: 110,
                              overflow: "hidden", fontFamily: "monospace",
                              lineHeight: 1.5, whiteSpace: "pre-wrap",
                            }}>
                              {(entry.code ?? "").slice(0, 400)}
                            </pre>
                            <div style={{
                              position: "absolute", bottom: 0, left: 0, right: 0, height: 36,
                              background: "linear-gradient(transparent,#0a0910)",
                              borderRadius: "0 0 7px 7px",
                            }} />
                          </div>
                        </>
                      )}

                      {/* Restore button */}
                      <button
                        onClick={() => { onRestore(entry); onClose(); }}
                        style={{
                          width: "100%", padding: "11px", borderRadius: 9, border: "none",
                          background: "linear-gradient(135deg,#8b5cf6,#6366f1)",
                          color: "#fff", fontSize: 13, fontWeight: 600, cursor: "pointer",
                          display: "flex", alignItems: "center", justifyContent: "center", gap: 7,
                          marginTop: 10,
                        }}
                      >
                        <RotateCcw size={14} />
                        Restore this generation
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {entries.length > 0 && (
          <div style={{
            padding: "11px 16px", borderTop: "1px solid #2d2a3d",
            fontSize: 11, color: "#334155", textAlign: "center",
            flexShrink: 0, background: "#0f0d1a",
          }}>
            Showing {filtered.length} of {entries.length} entries · last 100 kept
          </div>
        )}
      </div>
    </>
  );
}