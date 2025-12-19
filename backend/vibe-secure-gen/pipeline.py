from stages.prompt import enhance_prompt
from stages.prompt_firewall import sanitize_prompt
from stages.llm import stream_code
from stages.semgrep_registry import run_semgrep_registry_over_blob

async def run_pipeline(prompt: str):
    """
    Main pipeline: sanitize -> enhance -> generate -> SAST
    Language is inferred by the LLM; no language parameter needed.
    """
    safe_prompt = sanitize_prompt(prompt or "")
    enh = enhance_prompt(safe_prompt)
    hardened = enh["text"]
    policy_version = enh["policy_version"]

    parts = []
    async for chunk in stream_code(hardened):
        parts.append(chunk)
    code_blob = "".join(parts).strip() or "// empty"

    semgrep = run_semgrep_registry_over_blob(code_blob)

    return {
        "code": code_blob,
        "report": {
            "policy_version": policy_version,
            "prompt_after_enhancement": hardened,
            "semgrep": semgrep,
        },
        "decision": "CODE_ONLY",
    }
