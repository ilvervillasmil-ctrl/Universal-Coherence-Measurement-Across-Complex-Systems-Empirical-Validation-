#!/usr/bin/env python3
"""
OMEGA DIARY PUBLISHER
Publica el estado fenomenológico del sistema en GitHub Issue #8 (Diario_de_Estado).

# SOURCE OF TRUTH RULE:
# omega_diary_publisher MUST NOT compute or infer system state.
# It must ONLY render the output of omega_report.py.

Omega Report = cálculo
Omega Diary  = presentación

Lee directamente desde diagnostics/OMEGA_REPORT.md o desde
diagnostics/omega_report_data.json si existe (formato estructurado).
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error


# =============================================================================
# SOURCE OF TRUTH RULE:
# omega_diary_publisher MUST NOT compute or infer system state.
# It must ONLY render the output of omega_report.py.
# =============================================================================

ISSUE_NUMBER = 8
REPO_OWNER   = "ilvervillasmil-ctrl"
REPO_NAME    = "Universal-Integration-System"

CURRENT_FILE    = Path(__file__).resolve()
DIAGNOSTICS_DIR = CURRENT_FILE.parent


# =============================================================================
# CARGA DESDE FUENTE DE VERDAD: omega_report.py
# =============================================================================

def load_omega_report() -> dict | None:
    """
    Carga los datos del sistema EXCLUSIVAMENTE desde la salida de omega_report.py.

    Prioridad:
      1. diagnostics/omega_report_data.json  (formato estructurado, preferido)
      2. diagnostics/OMEGA_REPORT.md         (parseo de markdown como fallback)

    NO realiza ningún cálculo. Solo lee y extrae.
    """
    json_path = DIAGNOSTICS_DIR / "omega_report_data.json"
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            print("INFO: Loaded from omega_report_data.json")
            return data
        except Exception as exc:
            print(f"WARNING: Could not parse omega_report_data.json — {exc}")

    md_path = DIAGNOSTICS_DIR / "OMEGA_REPORT.md"
    if not md_path.exists():
        print("ERROR: Neither omega_report_data.json nor OMEGA_REPORT.md found.")
        print("       Run omega_report.py first to generate the source of truth.")
        return None

    try:
        text = md_path.read_text(encoding="utf-8")
        return _parse_omega_report_md(text)
    except Exception as exc:
        print(f"ERROR: Could not parse OMEGA_REPORT.md — {exc}")
        return None

def _extract_md_value(text: str, label: str) -> str | None:
    """Extrae el valor de una fila de tabla markdown: | label | valor |"""
    pattern = re.compile(
        r"\|\s*" + re.escape(label) + r"\s*\|\s*`?([^`|\n]+?)`?\s*|",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip().lstrip("*").rstrip("*").strip()
    return None

def _parse_omega_report_md(text: str) -> dict:
    """
    Parsea OMEGA_REPORT.md y extrae los campos clave.
    Solo lectura — no calcula nada.
    """

    def extract(label: str) -> str | None:
        return _extract_md_value(text, label)

    c_struct_raw = extract("C_struct (Estructural)")
    c_struct = float(c_struct_raw) if c_struct_raw else None

    c_global_raw = extract("C_global (Normalizada)")
    c_global_norm = float(c_global_raw) if c_global_raw else None

    c_ci_raw = extract("C_CI (Pass Rate)")
    c_ci = float(c_ci_raw) if c_ci_raw else None

    l7_raw = extract("L7 (Integración)")
    l7 = float(l7_raw) if l7_raw else None

    phi_raw = extract("φ_eff (Fricción)")
    phi_eff = float(phi_raw) if phi_raw else None

    codigo = None
    code_match = re.search(r"\|\s*Códig\s*\|\s*\*?\*?(\d{4})\*?\*?\s*|", text)
    if code_match:
        codigo = code_match.group(1).strip()

    estado = None
    nombre_match = re.search(r"\|\s*Denominación\s*\|\s*\*?\*?([^|*\n]+?)\*?\*?\s*|", text)
    if nombre_match:
        estado = nombre_match.group(1).strip()

    pheno_match = re.search(r"\|\s*Estado\s*\|\s*\*?\*?([^|*\n]+?)\*?\*?\s*|", text)
    pheno = pheno_match.group(1).strip() if pheno_match else None

    pass_rate = None
    pr_match = re.search(r"\|\s*Pass Rate\s*\|\s*([\d.]+)%", text)
    if pr_match:
        pass_rate = float(pr_match.group(1))

    total_match   = re.search(r"\|\s*Total Tests\s*\|\s*\*?\*?(\d+)\*?\*?\s*|", text)
    passed_match  = re.search(r"\|\s*Passed\s*\|\s*(\d+)\s*|", text)
    failed_match  = re.search(r"\|\s*Failed\s*\|\s*(\d+)\s*|", text)
    skipped_match = re.search(r"\|\s*Skipped\s*\|\s*(\d+)\s*|", text)

    return {
        "C_struct":      c_struct,
        "C_global_norm": c_global_norm,
        "C_CI":          c_ci,
        "L7":            l7,
        "phi_eff":       phi_eff,
        "codigo":        codigo,
        "estado":        estado,
        "pheno":         pheno,
        "pass_rate":     pass_rate,
        "total":         int(total_match.group(1))   if total_match   else 0,
        "passed":        int(passed_match.group(1))  if passed_match  else 0,
        "failed":        int(failed_match.group(1))  if failed_match else 0,
        "skipped":       int(skipped_match.group(1)) if skipped_match else 0,
    }


# =============================================================================
# RENDER — solo presenta, nunca calcula
# =============================================================================
def fmt(v, decimals=4) -> str:
    """Format a numeric value or return 'N/A'."""
    if v is None:
        return "N/A"
    return "{:.{}f}".format(v, decimals)


def format_diary_entry(report: dict, sha: str) -> str:
    """
    Construye el cuerpo del comentario para el Diario_de_Estado.

    RENDER ONLY — no computa ningún valor, solo formatea lo que recibe.
    Todos los valores provienen de omega_report.py (fuente de verdad).
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    c_struct      = report.get("C_struct")
    c_global_norm = report.get("C_global_norm")
    c_ci          = report.get("C_CI")
    l7            = report.get("L7")
    phi_eff       = report.get("phi_eff")
    codigo        = report.get("codigo",  "N/A")
    estado        = report.get("estado",  "N/A")
    pheno         = report.get("pheno",   "")
    pass_rate     = report.get("pass_rate")
    total         = report.get("total",   0)
    passed        = report.get("passed",  0)
    failed        = report.get("failed",  0)
    skipped       = report.get("skipped", 0)

    # Pre-compute formatted strings — avoids any f-string brace escaping issues
    c_struct_str      = fmt(c_struct)
    c_global_norm_str = fmt(c_global_norm)
    c_ci_str          = fmt(c_ci)
    l7_str            = fmt(l7, 6)
    phi_eff_str       = fmt(phi_eff, 6)
    pass_rate_str     = fmt(pass_rate, 4)

    lines = [
        "## Ω — Hora Ω: " + now,
        "",
        "**Estado Fenomenológico**: " + str(pheno),
        "> " + str(estado),
        "",
        "**Código Diagnóstico**: `" + str(codigo) + "`",
        "",
        "> ⚠️ Fuente de verdad: `omega_report.py` — este diary NO recalcula.",
        "",
        "### Métricas del Sistema (desde OMEGA_REPORT)",
        "",
        "| Métrica | Valor | Origen |",
        "|---------|-------|--------|",
        "| C_struct (Coherencia Estructural) | `" + c_struct_str      + "` | omega_report.py |",
        "| C_global_norm (Normalizada)       | `" + c_global_norm_str + "` | omega_report.py |",
        "| C_CI (Pass Rate proxy)            | `" + c_ci_str          + "` | omega_report.py |",
        "| L7 (Integración Total)            | `" + l7_str            + "` | omega_report.py |",
        "| φ_eff (Fricción Efectiva)         | `" + phi_eff_str       + "` | omega_report.py |",
        "| Pass Rate                         | `" + pass_rate_str     + "%` | omega_report.py |",
        "| Commit SHA                        | `" + str(sha)          + "` | CI |",
        "",
        "### Tests",
        "",
        "| Categoría | Cantidad |",
        "|-----------|----------|",
        "| Total     | **" + str(total)   + "** |",
        "| Pasados   | "   + str(passed)  + " |",
        "| Fallidos  | "   + str(failed)  + " |",
        "| Skipeados | "   + str(skipped) + " |",
        "",
        "---",
        "*Publicado automáticamente por Omega CI — renderer puro, sin cálculos propios.*",
    ]

    return "\n".join(lines)

# =============================================================================
# PUBLICACIÓN EN GITHUB
# =============================================================================
def publish_to_github(body: str) -> bool:
    """Publica un comentario en el Issue #8 del repositorio."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("WARNING: GITHUB_TOKEN not set — skipping publication (non-fatal).")
        return False

    url = (
        "https://api.github.com/repos/"
        + REPO_OWNER + "/" + REPO_NAME
        + "/issues/" + str(ISSUE_NUMBER) + "/comments"
    )
    headers = {
        "Authorization": "Bearer " + token,
        "Accept":        "application/vnd.github.v3+json",
        "Content-Type":  "application/json",
        "User-Agent":    "Omega-CI",
    }
    data = json.dumps({"body": body}).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            result   = json.loads(response.read().decode("utf-8"))
            html_url = result.get("html_url", "N/A")
            print("✓ Diario_de_Estado updated — " + html_url)
            return True
    except urllib.error.HTTPError as exc:
        body_err = exc.read().decode("utf-8", errors="replace")
        print("WARNING: HTTP " + str(exc.code) + " publishing to issue #" + str(ISSUE_NUMBER) + " — " + exc.reason)
        print("  Response: " + body_err)
        return False
    except Exception as exc:
        print("WARNING: Could not publish to issue #" + str(ISSUE_NUMBER) + " — " + str(exc))
        return False

# =============================================================================
# MAIN
# =============================================================================
def main() -> None:
    print()
    print("=" * 60)
    print("OMEGA DIARY PUBLISHER  [renderer — no calculator]")
    print("=" * 60)

    sha = os.getenv("GITHUB_SHA", "local")[:7]

    report = load_omega_report()
    if report is None:
        print("ERROR: Could not load Omega Report — skipping diary publication.")
        sys.exit(0)

    if report.get("codigo") is None:
        print("WARNING: 'codigo' not found in report — diary may show incomplete data.")
    if report.get("C_struct") is None:
        print("WARNING: 'C_struct' not found in report — diary may show incomplete data.")

    print("INFO: codigo   = " + str(report.get("codigo")))
    print("INFO: C_struct = " + str(report.get("C_struct")))
    print("INFO: L7       = " + str(report.get("L7")))

    entry = format_diary_entry(report, sha)

    print()
    print(entry)
    print()

    success = publish_to_github(entry)

    if success:
        print("✓ Omega Diary published successfully.")
    else:
        print("⚠ Diary publication skipped or failed (non-fatal).")

    sys.exit(0)


if __name__ == "__main__":
    main()
