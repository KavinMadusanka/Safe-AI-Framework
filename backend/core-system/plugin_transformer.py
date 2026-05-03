"""
plugin_transformer.py  (v5)
---------------------------
Converts AI-generated React components into the plugin runner format.
No API key required — fully local conversion.

Key fix in v5: JSX is extracted ONLY from inside the return(...) block.
All JS logic (useState, handlers) is re-built as vanilla JS separately.
Nothing from the JS logic section leaks into the HTML output.
"""

from __future__ import annotations
import re
import logging

log = logging.getLogger("plugin_transformer")


# ─────────────────────────────────────────────────────────────
# Detection
# ─────────────────────────────────────────────────────────────

_ALREADY_TRANSFORMED = [
    re.compile(r"async\s+function\s+run\s*\(\s*input"),
    re.compile(r"function\s+run\s*\(\s*input"),
    re.compile(r"module\.exports\s*=\s*\{?\s*run"),
    re.compile(r"exports\.run\s*="),
    re.compile(r"export\s+\{?\s*run\s*\}?"),
]

_REACT_PATTERNS = [
    re.compile(r"import\s+React"),
    re.compile(r"from\s+['\"]react['\"]"),
    re.compile(r"export\s+default\s+function\s+\w+"),
    re.compile(r"export\s+default\s+\w+\s*;?\s*$", re.MULTILINE),
    re.compile(r"useState\s*\("),
    re.compile(r"useEffect\s*\("),
    re.compile(r"return\s*\(\s*\n?\s*<"),
]

_HTML_PATTERN = re.compile(
    r"^\s*<!DOCTYPE\s+html|^\s*<html", re.IGNORECASE
)


def _is_already_transformed(src: str) -> bool:
    return any(p.search(src) for p in _ALREADY_TRANSFORMED)

def _is_plain_html(src: str) -> bool:
    return bool(_HTML_PATTERN.search(src[:500]))

def _is_react_component(src: str) -> bool:
    return any(p.search(src) for p in _REACT_PATTERNS)


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

def transform_plugin_entry(
    source: str, filename: str = "entry.js"
) -> tuple[str, bool]:
    """
    Returns (transformed_source, was_transformed).
    Priority:
      1. Already runner format  -> pass-through
      2. Plain HTML             -> wrap in run()
      3. React/JSX              -> convert to vanilla HTML+JS, wrap
      4. Plain JS               -> stub wrapper
    """
    if _is_already_transformed(source):
        log.info("[TRANSFORMER] %s - already runner format", filename)
        return source, False

    if _is_plain_html(source):
        log.info("[TRANSFORMER] %s - plain HTML", filename)
        return _wrap_html(source, filename, "plain HTML"), True

    if _is_react_component(source):
        log.info("[TRANSFORMER] %s - React/JSX component", filename)
        return _convert_react(source, filename), True

    log.info("[TRANSFORMER] %s - plain JS stub", filename)
    return _plain_js_stub(source, filename), True


# ─────────────────────────────────────────────────────────────
# React → Vanilla HTML + JS
# ─────────────────────────────────────────────────────────────

def _convert_react(source: str, filename: str) -> str:
    """
    Full local conversion of a React functional component.

    Steps:
      1. Extract CSS from <style>{`...`}</style>
      2. Extract useState declarations
      3. Extract handler functions (const handleX = ...)
      4. Extract ONLY the JSX inside return(...)
      5. Convert JSX → plain HTML
      6. Build vanilla JS (state vars + setters + handlers + _render)
      7. Assemble and wrap in run()
    """

    # 1. CSS
    css = _extract_css(source)

    # 2. State variables
    state_vars = _extract_state_vars(source)

    # 3. Handlers
    handlers = _extract_handlers(source)

    # 4. JSX block — ONLY what is inside return(...)
    jsx = _extract_jsx_return(source)

    # 5. JSX → HTML
    html_body = _jsx_to_html(jsx)

    # 6. Vanilla JS
    js = _build_js(state_vars, handlers)

    # 7. Assemble
    parts: list[str] = []
    if css:
        parts.append(f"<style>\n{css}\n</style>")
    parts.append(html_body)
    if js:
        parts.append(f"<script>\n{js}\n</script>")

    final_html = "\n\n".join(p for p in parts if p.strip())
    return _wrap_html(final_html, filename, "React component")


# ─────────────────────────────────────────────────────────────
# Step 1 — extract CSS
# ─────────────────────────────────────────────────────────────

def _extract_css(source: str) -> str:
    m = re.search(r"<style>\s*\{`(.*?)`\s*\}</style>", source, re.DOTALL)
    return m.group(1).strip() if m else ""


# ─────────────────────────────────────────────────────────────
# Step 2 — extract useState declarations
# ─────────────────────────────────────────────────────────────

# Matches both simple and object defaults:
#   const [x, setX] = useState(false);
#   const [form, setForm] = useState({ name: "", email: "" });
_USE_STATE_RE = re.compile(
    r"const\s+\[(\w+)\s*,\s*(\w+)\]\s*=\s*useState\s*\(([\s\S]*?)\)\s*;",
)

def _extract_state_vars(source: str) -> list[tuple[str, str, str]]:
    """Returns list of (varName, setterName, defaultValueJS)."""
    results = []
    for m in _USE_STATE_RE.finditer(source):
        var     = m.group(1)
        setter  = m.group(2)
        default = m.group(3).strip()
        results.append((var, setter, default))
    return results


# ─────────────────────────────────────────────────────────────
# Step 3 — extract handler functions
# ─────────────────────────────────────────────────────────────

def _extract_handlers(source: str) -> list[tuple[str, str, str]]:
    """
    Returns list of (fnName, params, bodyJS) for:
      const handleX = (params) => { body };
      const handleX = (params) => { body };   — multiline
    Skips useState / useEffect lines.
    """
    results: list[tuple[str, str, str]] = []

    # Arrow functions assigned to const
    pattern = re.compile(
        r"const\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>\s*\{([\s\S]*?)\n\s*\};?",
    )
    for m in pattern.finditer(source):
        name   = m.group(1)
        params = m.group(2).strip()
        body   = m.group(3)

        # Skip hooks and the component function itself
        if name in ("useState", "useEffect"):
            continue
        # Skip if this is a useState line that leaked in
        if "useState" in body and len(body.strip()) < 20:
            continue

        results.append((name, params, _clean_js_body(body)))

    return results


def _clean_js_body(body: str) -> str:
    """
    Clean a React handler body so it works as vanilla JS.
    Keeps setState calls (our vanilla setters handle them),
    keeps preventDefault, removes JSX markup.
    """
    b = body

    # Remove JSX: anything that looks like <Tag ... > or </Tag>
    b = re.sub(r"<[A-Za-z][^>]*/?>", "", b)
    b = re.sub(r"</[A-Za-z][^>]*>",  "", b)
    b = re.sub(r"<>\s*",  "", b)
    b = re.sub(r"</>\s*", "", b)

    # Remove JSX comments
    b = re.sub(r"\{/\*.*?\*/\}", "", b, flags=re.DOTALL)

    return b


# ─────────────────────────────────────────────────────────────
# Step 4 — extract JSX from inside return(...)
# ─────────────────────────────────────────────────────────────

def _extract_jsx_return(source: str) -> str:
    """
    Finds the LAST return (...) block in the source
    (the component's render return, not an early return).
    Uses bracket counting so it handles nested parens correctly.
    Returns only the content inside the outer parens.
    """
    # Find all positions of "return ("
    matches = list(re.finditer(r"\breturn\s*\(", source))
    if not matches:
        # Try: return <div...>  (no parens)
        m2 = re.search(r"\breturn\s+(<[\s\S]+)", source)
        if m2:
            # Take until end of component (last };)
            candidate = m2.group(1)
            # strip trailing }; lines
            candidate = re.sub(r"\n\s*\}\s*;?\s*$", "", candidate.rstrip())
            return candidate.strip()
        return source

    # Use the last return( — that's the JSX render return
    match = matches[-1]
    start = match.end()       # position just after "return ("
    depth = 1
    i     = start
    n     = len(source)

    while i < n and depth > 0:
        if source[i] == "(":
            depth += 1
        elif source[i] == ")":
            depth -= 1
        i += 1

    jsx = source[start : i - 1].strip()
    return jsx


# ─────────────────────────────────────────────────────────────
# Step 5 — JSX → plain HTML
# ─────────────────────────────────────────────────────────────

def _jsx_to_html(jsx: str) -> str:
    h = jsx

    # Remove <style>{`...`}</style> (already extracted)
    h = re.sub(r"<style>\s*\{`[\s\S]*?`\s*\}</style>", "", h)

    # Remove JSX comments {/* ... */}
    h = re.sub(r"\{/\*[\s\S]*?\*/\}", "", h)

    # Remove fragment wrappers
    h = re.sub(r"<>\s*",  "", h)
    h = re.sub(r"</>\s*", "", h)

    # className -> class
    h = re.sub(r'\bclassName=', "class=", h)

    # ── Event handlers ──────────────────────────────────────
    # onChange={(e) => handleChange("field", e.target.value)}
    # -> oninput="handleChange('field', this.value)"
    def _evt(attr_out: str):
        def replacer(m: re.Match) -> str:
            expr = m.group(1).strip()
            converted = _jsx_handler_to_inline(expr)
            return f'{attr_out}="{converted}"'
        return replacer

    h = re.sub(r'\bonChange=\{([\s\S]*?)\}(?=\s|>)',  _evt("oninput"),  h)
    h = re.sub(r'\bonSubmit=\{([\s\S]*?)\}(?=\s|>)',
               lambda m: f'onsubmit="{_jsx_handler_to_inline(m.group(1))}; return false;"', h)
    h = re.sub(r'\bonClick=\{([\s\S]*?)\}(?=\s|>)',   _evt("onclick"),  h)
    h = re.sub(r'\bonBlur=\{([\s\S]*?)\}(?=\s|>)',    _evt("onblur"),   h)
    h = re.sub(r'\bonFocus=\{([\s\S]*?)\}(?=\s|>)',   _evt("onfocus"),  h)

    # value={...} -> remove (vanilla forms read from DOM directly)
    h = re.sub(r'\bvalue=\{[^}]+\}', "", h)

    # checked={...} -> remove
    h = re.sub(r'\bchecked=\{[^}]+\}', "", h)

    # Remove self-closing uppercase component tags <Component />
    h = re.sub(r"<[A-Z]\w*[^>]*/\s*>", "", h)

    # Remove paired uppercase component tags <Component>...</Component>
    h = re.sub(r"<[A-Z]\w*[^>]*>[\s\S]*?</[A-Z]\w*>", "", h)

    # ── Ternary blocks ──────────────────────────────────────
    # {cond ? (<true>) : (<false>)}
    h = _convert_ternaries(h)

    # ── Inline JSX expressions ──────────────────────────────
    # {form.name} -> <span class="__expr" data-expr="form.name"></span>
    def _expr(m: re.Match) -> str:
        inner = m.group(1).strip()
        # skip if it looks like it still contains JS logic
        if "\n" in inner or "=>" in inner or "(" in inner:
            return ""
        safe_id = re.sub(r"[^a-zA-Z0-9_]", "_", inner)
        return f'<span id="expr_{safe_id}" data-expr="{inner}"></span>'

    h = re.sub(r"\{([^{}]+)\}", _expr, h)

    # Clean up any stray { } that remain
    h = re.sub(r"[{}]", "", h)

    # Collapse blank lines
    h = re.sub(r"\n{3,}", "\n\n", h)

    return h.strip()


def _jsx_handler_to_inline(expr: str) -> str:
    """
    Convert a JSX event expression to an inline HTML event string.

    Examples:
      (e) => handleChange("name", e.target.value)
        -> handleChange('name', this.value)
      handleSubmit
        -> handleSubmit(event)
      (e) => { e.preventDefault(); handleSubmit(e); }
        -> handleSubmit(event)
    """
    e = expr.strip()

    # Arrow with block body: (e) => { ... }
    block = re.match(r"\(?\s*(\w+)\s*\)?\s*=>\s*\{([\s\S]+)\}", e)
    if block:
        param = block.group(1)
        body  = block.group(2).strip()
        # Remove e.preventDefault() — handled by return false in onsubmit
        body = re.sub(r"\b" + re.escape(param) + r"\.preventDefault\(\)\s*;?", "", body)
        body = body.replace(param + ".", "event.").strip().rstrip(";")
        # If multiple statements remain, keep first meaningful one
        stmts = [s.strip() for s in body.split(";") if s.strip()]
        body  = stmts[0] if stmts else ""
        return body

    # Arrow with expression body: (e) => handleChange("x", e.target.value)
    arrow = re.match(r"\(?\s*(\w+)\s*\)?\s*=>\s*(.+)", e)
    if arrow:
        param = arrow.group(1)
        body  = arrow.group(2).strip().rstrip(";")
        # Replace param.target.value with this.value for input events
        body  = re.sub(re.escape(param) + r"\.target\.value", "this.value",  body)
        body  = re.sub(re.escape(param) + r"\.target\.checked","this.checked",body)
        body  = body.replace(param + ".", "event.")
        return body

    # Bare function reference: handleSubmit
    if re.match(r"^\w+$", e):
        return f"{e}(event)"

    return e


def _convert_ternaries(h: str) -> str:
    """
    Convert {cond ? (<trueJSX>) : (<falseJSX>)} to show/hide divs.
    Works for both  (<jsx>)  and  <jsx>  forms.
    """
    counter = [0]

    def replacer(m: re.Match) -> str:
        counter[0] += 1
        cond   = m.group(1).strip()
        branch_t = m.group(2).strip().strip("()")
        branch_f = m.group(3).strip().strip("()")
        tid = f"ternary_{counter[0]}"
        safe_cond = re.sub(r"[^a-zA-Z0-9_]", "_", cond)
        return (
            f'<div id="{tid}_true"  data-ternary-cond="{cond}" data-ternary-id="{tid}">'
            f'{branch_t}</div>'
            f'<div id="{tid}_false" data-ternary-id="{tid}" style="display:none">'
            f'{branch_f}</div>'
        )

    # Match {cond ? (...) : (...)} or {cond ? <...> : <...>}
    pattern = re.compile(
        r"\{\s*(\w+)\s*\?\s*"          # {cond ?
        r"(\([^()]*(?:\([^()]*\))*[^()]*\)|<[\s\S]*?>)\s*"   # (trueBlock) or <tag>
        r":\s*"                         # :
        r"(\([^()]*(?:\([^()]*\))*[^()]*\)|<[\s\S]*?>)\s*"   # (falseBlock) or <tag>
        r"\}",
        re.DOTALL
    )
    return pattern.sub(replacer, h)


# ─────────────────────────────────────────────────────────────
# Step 6 — build vanilla JS
# ─────────────────────────────────────────────────────────────

def _build_js(
    state_vars: list[tuple[str, str, str]],
    handlers:   list[tuple[str, str, str]],
) -> str:
    if not state_vars and not handlers:
        return ""

    lines: list[str] = []

    # ── State variables ─────────────────────────────────────
    if state_vars:
        lines.append("// State")
        for var, setter, default in state_vars:
            lines.append(f"var {var} = {default};")
        lines.append("")

        # ── Setter functions ────────────────────────────────
        lines.append("// Setters")
        for var, setter, _ in state_vars:
            lines.append(f"""function {setter}(newVal) {{
  if (typeof newVal === 'function') {{
    {var} = newVal({var});
  }} else {{
    {var} = newVal;
  }}
  _render();
}}""")
        lines.append("")

        # ── _render ─────────────────────────────────────────
        lines.append("// Render — update DOM after state changes")
        lines.append("function _render() {")

        # Update <span data-expr="..."> elements
        for var, _, _ in state_vars:
            # simple var
            safe = re.sub(r"[^a-zA-Z0-9_]", "_", var)
            lines.append(f"""  (function() {{
    var el = document.getElementById('expr_{safe}');
    if (el) el.textContent = {var};
  }})();""")

        # Update ternary show/hide
        lines.append("""
  // Ternary show/hide
  document.querySelectorAll('[data-ternary-cond]').forEach(function(el) {
    var cond = el.getAttribute('data-ternary-cond');
    var tid  = el.getAttribute('data-ternary-id');
    var result;
    try { result = eval(cond); } catch(e) { result = false; }
    var trueEl  = document.getElementById(tid + '_true');
    var falseEl = document.getElementById(tid + '_false');
    if (trueEl)  trueEl.style.display  = result ? '' : 'none';
    if (falseEl) falseEl.style.display = result ? 'none' : '';
  });""")

        lines.append("}")
        lines.append("")

    # ── Handler functions ────────────────────────────────────
    if handlers:
        lines.append("// Handlers")
        for name, params, body in handlers:
            lines.append(f"function {name}({params}) {{{body}\n}}")
            lines.append("")

    # ── Init ─────────────────────────────────────────────────
    lines.append("// Init")
    lines.append("document.addEventListener('DOMContentLoaded', function() {")
    if state_vars:
        lines.append("  _render();")
    lines.append("});")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Wrap in runner format
# ─────────────────────────────────────────────────────────────

def _escape_template(content: str) -> str:
    return (
        content
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )


def _wrap_html(html: str, filename: str, label: str = "HTML") -> str:
    escaped = _escape_template(html)
    return (
        f"// Auto-converted from {label}: {filename}\n"
        f"// Converted by safe-Ai-framework plugin_transformer v5\n\n"
        f"function renderHtml() {{\n"
        f"  return `{escaped}`;\n"
        f"}}\n\n"
        f"async function run(input, ctx) {{\n"
        f"  return {{ html: renderHtml() }};\n"
        f"}}\n\n"
        f"module.exports = {{ run }};\n"
    )


# ─────────────────────────────────────────────────────────────
# Plain JS stub
# ─────────────────────────────────────────────────────────────

def _plain_js_stub(source: str, filename: str) -> str:
    safe = _escape_template(source)
    return (
        f"// Auto-wrapped: {filename}\n"
        f"// Converted by safe-Ai-framework plugin_transformer v5\n\n"
        f"async function run(input, ctx) {{\n"
        f"  return {{\n"
        f"    html: `<div style='font-family:sans-serif;padding:20px'>\n"
        f"      <h2>Plugin not converted</h2>\n"
        f"      <p>File <strong>{filename}</strong> could not be auto-converted.</p>\n"
        f"      <p>Export an async <code>run(input, ctx)</code> returning "
        f"<code>{{{{ html: '...' }}}}</code>.</p>\n"
        f"    </div>`,\n"
        f"  }};\n"
        f"}}\n\n"
        f"module.exports = {{ run }};\n"
    )