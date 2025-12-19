import os
import re
from typing import Dict, Tuple, List

FENCE_RE = re.compile(r"^```([a-zA-Z0-9_+-]*)\s*\n([\s\S]*?)\n```$", re.M)

EXT_TO_LANG = {
    ".js": "javascript", ".jsx": "javascript",
    ".ts": "typescript", ".tsx": "typescript",
    ".html": "html", ".css": "css",

    ".java": "java", ".kt": "kotlin", ".kts": "kotlin",
    ".py": "python", ".go": "go", ".rb": "ruby",
    ".php": "php", ".cs": "csharp", ".rs": "rust",
    ".scala": "scala", ".c": "c", ".cpp": "cpp", ".cc": "cpp",

    ".xml": "xml", ".json": "json", ".yml": "yaml", ".yaml": "yaml", ".sql": "sql",
    ".gradle": "kotlin", ".groovy": "groovy",
    ".properties": "text", ".env": "text",
    ".txt": "text", ".md": "text",
}

def strip_fence(text: str) -> Tuple[str, str]:
    m = FENCE_RE.search(text.strip())
    if not m:
        return "", text.strip()
    lang = (m.group(1) or "").strip().lower()
    inner = (m.group(2) or "").strip()
    return lang, inner

def _guess_single_fallback_name(fence_lang: str) -> str:
    if fence_lang in ("java","kotlin","python","go","php","ruby","csharp","rust","scala","javascript","typescript"):
        ext = {
            "java": ".java","kotlin": ".kt","python": ".py","go": ".go","php": ".php",
            "ruby": ".rb","csharp": ".cs","rust": ".rs","scala": ".scala",
            "javascript": ".js","typescript": ".ts",
        }[fence_lang]
        return f"Main{ext}"
    return "Main.txt"

def split_files(inner: str, fence_lang: str) -> Dict[str, str]:
    sep = re.compile(r"^===\s*FILE:\s*(.+?)\s*===\s*$")
    lines = inner.splitlines()
    files: Dict[str, str] = {}
    current_path = None
    buf: List[str] = []

    def flush():
        nonlocal current_path, buf
        if current_path:
            files[current_path] = "\n".join(buf).rstrip()
        current_path, buf = None, []

    for ln in lines:
        m = sep.match(ln)
        if m:
            flush()
            current_path = m.group(1).strip().replace("\\", "/")
            continue
        buf.append(ln)
    flush()

    if files:
        return files

    # single-file fallback
    fallback = _guess_single_fallback_name(fence_lang)
    return {fallback: inner}

def materialize_files(root_dir: str, code_blob: str) -> Dict[str, str]:
    fence_lang, inner = strip_fence(code_blob)
    file_map = split_files(inner, fence_lang)

    abs_map: Dict[str, str] = {}
    for rel, content in file_map.items():
        abs_path = os.path.join(root_dir, *rel.split("/"))
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        abs_map[rel] = abs_path
    return abs_map

def detect_languages(rel_paths: List[str], fence_lang: str) -> List[str]:
    langs = set()
    if fence_lang:
        langs.add(fence_lang.lower())

    for rel in rel_paths:
        _, ext = os.path.splitext(rel.lower())
        lang = EXT_TO_LANG.get(ext)
        if lang:
            langs.add(lang)

    if "js" in langs:
        langs.discard("js"); langs.add("javascript")
    if "ts" in langs:
        langs.discard("ts"); langs.add("typescript")

    return sorted(langs)
