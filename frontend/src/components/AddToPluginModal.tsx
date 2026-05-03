import { useState } from "react";
import { X, FolderPlus, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

// ── Config ──────────────────────────────────────────────────────────────────
const CORE_API = import.meta.env.VITE_API_URL ?? "http://localhost:8012";

// ── Types ────────────────────────────────────────────────────────────────────
type Props = {
  open:    boolean;
  code:    string;          // the generated code to save as a plugin
  onClose: () => void;
};

type Status = "idle" | "saving" | "success" | "error";

// ── Helpers ──────────────────────────────────────────────────────────────────
function slugify(raw: string): string {
  return raw
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

// ── Component ─────────────────────────────────────────────────────────────────
export default function AddToPluginModal({ open, code, onClose }: Props) {
  const [slug,        setSlug]        = useState("");
  const [description, setDescription] = useState("");
  const [status,      setStatus]      = useState<Status>("idle");
  const [errorMsg,    setErrorMsg]    = useState("");

  if (!open) return null;

  function handleClose() {
    // Reset form when closing so next open is clean
    setSlug("");
    setDescription("");
    setStatus("idle");
    setErrorMsg("");
    onClose();
  }

  async function handleSave() {
    const cleanSlug = slugify(slug);

    if (!cleanSlug) {
      setErrorMsg("Slug name is required.");
      setStatus("error");
      return;
    }
    if (!description.trim()) {
      setErrorMsg("Description is required.");
      setStatus("error");
      return;
    }

    setStatus("saving");
    setErrorMsg("");

    try {
      // ── Step 1: Save entry.js (the generated code) ─────────────────────
      // The backend plugin_transformer will auto-convert React/JSX → run() format.
      const entryRes = await fetch(
        `${CORE_API}/core/plugin/new?path=${encodeURIComponent(`${cleanSlug}/entry.js`)}`,
        {
          method:  "POST",
          headers: { "Content-Type": "text/plain" },
          body:    code,
        }
      );
      if (!entryRes.ok) {
        const err = await entryRes.json().catch(() => ({}));
        throw new Error(err?.detail ?? `entry.js save failed (${entryRes.status})`);
      }

      // ── Step 2: Save manifest.json ──────────────────────────────────────
      const manifest = {
        name:        cleanSlug,
        description: description.trim(),
        version:     "1.0.0",
        entry:       "entry.js",
        created_at:  new Date().toISOString(),
      };

      const manifestRes = await fetch(
        `${CORE_API}/core/plugin/new?path=${encodeURIComponent(`${cleanSlug}/manifest.json`)}`,
        {
          method:  "POST",
          headers: { "Content-Type": "text/plain" },
          body:    JSON.stringify(manifest, null, 2),
        }
      );
      if (!manifestRes.ok) {
        const err = await manifestRes.json().catch(() => ({}));
        throw new Error(err?.detail ?? `manifest.json save failed (${manifestRes.status})`);
      }

      setStatus("success");
    } catch (e: any) {
      setErrorMsg(e?.message ?? "Unknown error");
      setStatus("error");
    }
  }

  // ── Render ───────────────────────────────────────────────────────────────
  const isBusy = status === "saving";

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={isBusy ? undefined : handleClose}
        style={{
          position: "fixed", inset: 0,
          background: "rgba(0,0,0,0.65)",
          backdropFilter: "blur(4px)",
          zIndex: 500,
        }}
      />

      {/* Modal box */}
      <div style={{
        position:     "fixed",
        top:          "50%",
        left:         "50%",
        transform:    "translate(-50%, -50%)",
        zIndex:       501,
        width:        440,
        background:   "#1a1328",
        border:       "1px solid #3d2060",
        borderRadius: 16,
        padding:      28,
        boxShadow:    "0 24px 64px rgba(0,0,0,0.6)",
      }}>

        {/* Header */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{
              width: 36, height: 36, borderRadius: 10,
              background: "linear-gradient(135deg,#4F0C87,#7c3aed)",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <FolderPlus size={18} color="#fff" />
            </div>
            <div>
              <div style={{ fontSize: 15, fontWeight: 700, color: "#ffffff" }}>
                Add to System
              </div>
              <div style={{ fontSize: 11, color: "#9a7ab5", marginTop: 2 }}>
                Save generated code as a runnable plugin
              </div>
            </div>
          </div>
          {!isBusy && (
            <button
              onClick={handleClose}
              style={{ background: "none", border: "none", cursor: "pointer", padding: 4, color: "#9a7ab5" }}
            >
              <X size={18} />
            </button>
          )}
        </div>

        {/* ── Success state ── */}
        {status === "success" ? (
          <div style={{ textAlign: "center", padding: "16px 0" }}>
            <CheckCircle2 size={48} color="#10b981" style={{ marginBottom: 14 }} />
            <div style={{ fontSize: 15, fontWeight: 700, color: "#10b981", marginBottom: 6 }}>
              Code saved successfully!
            </div>
            <div style={{ fontSize: 12, color: "#9a7ab5", marginBottom: 24, lineHeight: 1.6 }}>
              <strong style={{ color: "#c4b5d6" }}>{slugify(slug)}</strong> is now in your Generated code system.
              <br />
              The code was auto-converted to the <code style={{ color: "#c084fc" }}>run(input, ctx)</code> format.
            </div>
            <button
              onClick={handleClose}
              style={{
                width: "100%", padding: "12px 20px", borderRadius: 10, border: "none",
                background: "#10b981", color: "#fff", fontSize: 14, fontWeight: 600, cursor: "pointer",
              }}
            >
              Done
            </button>
          </div>
        ) : (
          /* ── Form state ── */
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>

            {/* Slug field */}
            <div>
              <label style={{
                display: "block", marginBottom: 6,
                fontSize: 11, fontWeight: 600, color: "#c4b5d6",
                textTransform: "uppercase", letterSpacing: "0.08em",
              }}>
                Slug Name <span style={{ color: "#ef4444" }}>*</span>
              </label>
              <input
                value={slug}
                onChange={(e) => {
                  setSlug(e.target.value);
                  if (status === "error") setStatus("idle");
                }}
                placeholder="e.g. about-page, product-list"
                disabled={isBusy}
                style={{
                  width: "100%", padding: "10px 14px", borderRadius: 9,
                  border: `1px solid ${status === "error" && !slug.trim() ? "#ef4444" : "#3d2060"}`,
                  background: "#150f24", color: "#ffffff",
                  fontSize: 13, outline: "none", boxSizing: "border-box",
                  opacity: isBusy ? 0.6 : 1,
                }}
                onFocus={(e) => (e.target.style.borderColor = "#4F0C87")}
                onBlur={(e)  => (e.target.style.borderColor = "#3d2060")}
              />
              {/* Live-preview the sanitised slug */}
              {slug.trim() && slugify(slug) !== slug.trim() && (
                <div style={{ fontSize: 10, color: "#9a7ab5", marginTop: 4 }}>
                  Will be saved as: <strong style={{ color: "#c084fc" }}>{slugify(slug)}</strong>
                </div>
              )}
            </div>

            {/* Description field */}
            <div>
              <label style={{
                display: "block", marginBottom: 6,
                fontSize: 11, fontWeight: 600, color: "#c4b5d6",
                textTransform: "uppercase", letterSpacing: "0.08em",
              }}>
                Description <span style={{ color: "#ef4444" }}>*</span>
              </label>
              <textarea
                rows={3}
                value={description}
                onChange={(e) => {
                  setDescription(e.target.value);
                  if (status === "error") setStatus("idle");
                }}
                placeholder="What does this plugin do?"
                disabled={isBusy}
                style={{
                  width: "100%", padding: "10px 14px", borderRadius: 9,
                  border: `1px solid ${status === "error" && !description.trim() ? "#ef4444" : "#3d2060"}`,
                  background: "#150f24", color: "#ffffff",
                  fontSize: 13, outline: "none", resize: "vertical",
                  boxSizing: "border-box", fontFamily: "inherit", lineHeight: 1.5,
                  opacity: isBusy ? 0.6 : 1,
                }}
                onFocus={(e) => (e.target.style.borderColor = "#4F0C87")}
                onBlur={(e)  => (e.target.style.borderColor = "#3d2060")}
              />
            </div>

            {/* Error banner */}
            {status === "error" && errorMsg && (
              <div style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "10px 14px", borderRadius: 8,
                background: "rgba(239,68,68,0.08)",
                border: "1px solid rgba(239,68,68,0.3)",
                fontSize: 12, color: "#fca5a5",
              }}>
                <AlertCircle size={14} color="#ef4444" style={{ flexShrink: 0 }} />
                {errorMsg}
              </div>
            )}

            {/* Buttons */}
            <div style={{ display: "flex", gap: 10, marginTop: 4 }}>
              <button
                onClick={handleClose}
                disabled={isBusy}
                style={{
                  flex: 1, padding: "12px 20px", borderRadius: 10,
                  border: "1px solid #3d2060", background: "transparent",
                  color: "#c4b5d6", fontSize: 14, fontWeight: 600,
                  cursor: isBusy ? "not-allowed" : "pointer", opacity: isBusy ? 0.5 : 1,
                }}
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={isBusy}
                style={{
                  flex: 2, padding: "12px 20px", borderRadius: 10, border: "none",
                  background: isBusy ? "#3d2060" : "linear-gradient(135deg,#4F0C87,#7c3aed)",
                  color: "#fff", fontSize: 14, fontWeight: 600,
                  cursor: isBusy ? "not-allowed" : "pointer",
                  display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
                }}
              >
                {isBusy
                  ? <><Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} /> Saving…</>
                  : <><FolderPlus size={16} /> Saved.</>
                }
              </button>
            </div>

            <style>{`@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }`}</style>
          </div>
        )}
      </div>
    </>
  );
}
