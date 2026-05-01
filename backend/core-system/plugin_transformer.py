"""
plugin_transformer.py
---------------------
Automatically converts AI-generated JavaScript/React components into
the plugin runner format that expects:

    async function run(input, ctx) { return { html: "..." }; }
    module.exports = { run };

Supports:
  - React functional components (JSX / inline styles)
  - Plain HTML-returning JS functions
  - Already-formatted plugins (pass-through, no double-transform)
"""

import re
import logging

log = logging.getLogger("plugin_transformer")

# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------

# Patterns that mean the file is ALREADY in runner format — skip transform
_ALREADY_TRANSFORMED = [
    re.compile(r"async\s+function\s+run\s*\(\s*input"),
    re.compile(r"function\s+run\s*\(\s*input"),
    re.compile(r"module\.exports\s*=\s*\{?\s*run"),
    re.compile(r"exports\.run\s*="),
    re.compile(r"export\s+\{?\s*run\s*\}?"),
]

# Patterns that indicate a React component file
_REACT_PATTERNS = [
    re.compile(r"import\s+React"),
    re.compile(r"from\s+['\"]react['\"]"),
    re.compile(r"<[A-Z][A-Za-z]*[\s/>]"),   # JSX uppercase component tag
    re.compile(r"<[a-z]+\s"),                # JSX lowercase HTML tag
    re.compile(r"return\s*\(?\s*<"),         # JSX return
    re.compile(r"export\s+default\s+\w+"),   # typical React export
]

# Captures the component name from "export default ComponentName"
_DEFAULT_EXPORT_RE = re.compile(r"export\s+default\s+(\w+)")

# Captures inline <style>{`...`}</style> blocks inside JSX
_JSX_STYLE_RE = re.compile(
    r"<style>\s*\{\s*`(.*?)`\s*\}\s*</style>",
    re.DOTALL,
)

# Captures plain <style>...</style> HTML strings
_HTML_STYLE_RE = re.compile(r"<style>(.*?)</style>", re.DOTALL)


def _is_already_transformed(source: str) -> bool:
    return any(p.search(source) for p in _ALREADY_TRANSFORMED)


def _is_react_component(source: str) -> bool:
    return any(p.search(source) for p in _REACT_PATTERNS)


# ---------------------------------------------------------------------------
# JSX → HTML conversion (lightweight, no Babel)
# ---------------------------------------------------------------------------

def _jsx_to_html(jsx: str) -> str:
    """
    Best-effort conversion of JSX markup to plain HTML strings.
    Handles the common patterns produced by AI code generators.
    """
    html = jsx

    # Remove import statements
    html = re.sub(r"^import\s+.*?;?\s*$", "", html, flags=re.MULTILINE)

    # Remove export default line
    html = re.sub(r"export\s+default\s+\w+\s*;?", "", html)

    # Remove the outer function / arrow function wrapper
    # e.g.  const Foo = () => {   or   function Foo() {
    html = re.sub(
        r"(?:const|let|var)\s+\w+\s*=\s*(?:\([^)]*\)\s*=>|function\s*\([^)]*\))\s*\{",
        "",
        html,
    )
    html = re.sub(r"^function\s+\w+\s*\([^)]*\)\s*\{", "", html, flags=re.MULTILINE)

    # Remove the React.FC / component type annotation lines
    html = re.sub(r":\s*React\.FC[^=]*=\s*", "= ", html)

    # Extract CSS from JSX-style <style>{`...`}</style>
    css_blocks: list[str] = []

    def _capture_jsx_style(m: re.Match) -> str:
        css_blocks.append(m.group(1).strip())
        return ""  # remove from HTML body

    html = _JSX_STYLE_RE.sub(_capture_jsx_style, html)

    # Remove JSX fragment wrappers <>  </>
    html = re.sub(r"<>\s*", "", html)
    html = re.sub(r"</>\s*", "", html)

    # Convert className= → class=
    html = re.sub(r'\bclassName=', 'class=', html)

    # Remove JSX comments {/* ... */}
    html = re.sub(r"\{/\*.*?\*/\}", "", html, flags=re.DOTALL)

    # Convert self-closing tags: <br /> → <br>
    html = re.sub(r"<(\w+)([^>]*)/\s*>", r"<\1\2>", html)

    # Remove JSX expression wrappers { expr } that aren't already attributes
    # e.g. {someVar} inline → keep text-like ones, drop the braces
    html = re.sub(r"\{([^{}]+)\}", r"\1", html)

    # Remove return( / return  at the top and the matching closing ) or }
    html = re.sub(r"\breturn\s*\(\s*", "", html)
    html = re.sub(r"\breturn\s+", "", html)

    # Trim trailing }) or }; from end of component body
    html = re.sub(r"\}\s*\)\s*;?\s*$", "", html.rstrip())
    html = re.sub(r"\}\s*;\s*$", "", html.rstrip())

    # Collapse multiple blank lines
    html = re.sub(r"\n{3,}", "\n\n", html)

    html = html.strip()

    # Re-inject CSS at the top
    if css_blocks:
        css = "\n".join(css_blocks)
        html = f"<style>\n{css}\n</style>\n{html}"

    return html


# ---------------------------------------------------------------------------
# Main transformer
# ---------------------------------------------------------------------------

def transform_plugin_entry(source: str, filename: str = "entry.js") -> tuple[str, bool]:
    """
    Given the raw *source* of a plugin file, return:
        (transformed_source: str, was_transformed: bool)

    If the file already has the correct format, it is returned unchanged.
    If it is a React/JSX component, it is converted to the runner format.
    Otherwise (plain JS with no recognizable shape) it is wrapped in a
    minimal run() stub that returns the source as a comment with an
    instruction message in html.
    """

    if _is_already_transformed(source):
        log.info("[TRANSFORMER] %s — already in runner format, skipping", filename)
        return source, False

    if _is_react_component(source):
        log.info("[TRANSFORMER] %s — detected React/JSX component, converting …", filename)
        return _transform_react(source, filename), True

    # Plain JS but not in runner format → wrap it
    log.info("[TRANSFORMER] %s — plain JS detected, wrapping in run() stub", filename)
    return _transform_plain_js(source, filename), True


def _transform_react(source: str, filename: str) -> str:
    """Convert a React functional component to the plugin runner format."""

    # Try to find the component's name for a helpful comment
    m = _DEFAULT_EXPORT_RE.search(source)
    component_name = m.group(1) if m else "Component"

    # Extract CSS from the JSX <style> tag before converting
    css_parts: list[str] = []

    def _grab_css(match: re.Match) -> str:
        css_parts.append(match.group(1).strip())
        return ""

    source_no_style = _JSX_STYLE_RE.sub(_grab_css, source)

    # Convert JSX body to HTML
    html_body = _jsx_to_html(source_no_style)

    # Re-attach extracted CSS at the very top of the html string
    if css_parts:
        css_combined = "\n".join(css_parts)
        html_content = f"<style>\n{css_combined}\n</style>\n{html_body}"
    else:
        html_content = html_body

    # Escape backticks and backslashes for template literal embedding
    html_escaped = html_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    transformed = f"""\
// Auto-converted from React component: {component_name}
// Original file: {filename}
// Converted by safe-Ai-framework plugin_transformer

function renderHtml() {{
  return `
{html_escaped}
  `;
}}

async function run(input, ctx) {{
  // input  : data sent from the API caller
  // ctx    : metadata / context provided by the plugin runner
  return {{ html: renderHtml() }};
}}

module.exports = {{ run }};
"""
    return transformed


def _transform_plain_js(source: str, filename: str) -> str:
    """
    Wrap an unrecognized plain JS file so the runner can at least load it.
    We embed the original source as a function body comment and return a
    placeholder HTML message so the developer knows what happened.
    """
    # Escape for template literal
    safe = source.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    transformed = f"""\
// Auto-wrapped plain JS: {filename}
// Converted by safe-Ai-framework plugin_transformer
// The original source is embedded below inside originalSource().

function originalSource() {{
  // ---- BEGIN ORIGINAL SOURCE ----
  /*
{safe}
  */
  // ---- END ORIGINAL SOURCE ----
}}

async function run(input, ctx) {{
  return {{
    html: `<div style="font-family:sans-serif;padding:20px;">
      <h2>⚠ Plugin Auto-Wrapped</h2>
      <p>The original file <strong>{filename}</strong> was not in the
      expected <code>run(input, ctx)</code> format and could not be parsed
      as a React component.</p>
      <p>Please edit <code>entry.js</code> to export an async
      <code>run(input, ctx)</code> function that returns
      <code>{{ html: "..." }}</code>.</p>
    </div>`,
  }};
}}

module.exports = {{ run }};
"""
    return transformed
