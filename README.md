# Agent-SlideLock: Deterministic Pre-Render TrueType Glyph-Metric Bounding-Box Solver, Disjoint AABB Spatial Partitioner, and Aspect-Ratio-Locked ECMA-376 OpenXML (`.PPTX`) Compiler

[![ECMA-376 OpenXML](https://img.shields.io/badge/ECMA--376-OpenXML%20.PPTX-blue)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)
[![Vertex AI Gemini](https://img.shields.io/badge/Vertex%20AI-Gemini%202.5%20%E2%86%92%203.8%20Flash-success)](https://cloud.google.com/vertex-ai)
[![Invariants](https://img.shields.io/badge/9%20Nanoscopic%20Invariants-100%25%20PASS-brightgreen)](#nine-nanoscopic-openxml-invariants)

**Author**: Aniket Agrawal (`aniketagrawal@google.com`) — Google Cloud Consulting / Professional Services Organization (PSO)

---

## Executive Overview

**`Agent-SlideLock`** is a deterministic ECMA-376 / ISO/IEC 29500 OpenXML (`.pptx`) compilation and verification engine designed for autonomous enterprise AI agents built on the **Google Cloud Vertex AI Agent Development Kit (ADK)** and frontier **Gemini** models (`gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3-flash-preview`, `gemini-2.5-pro`, and `gemini-2.5-flash`).

Unlike standard LLM-to-PowerPoint pipelines that rely on client-side `<a:normAutofit/>` (`MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`) heuristics—which cause jarring font-shrinkage inconsistencies across sibling cards—or unchecked `<a:noAutofit/>` locks that overflow vertically and horizontally, `Agent-SlideLock` solves all **8 Enterprise OpenXML Distortions (`D1–D8`)** and guarantees **9 Nanoscopic Mathematical Invariants** directly at the OpenXML binary ZIP/XML layer prior to file serialization:

1. **Pre-Render TrueType Glyph-Metric Solver (`hmtx`/`cmap`)**: Queries exact TrueType glyph advance widths, chunks unbroken technical tokens (130+ char HTTPS URLs, SHA-256 digests, SAP OData paths) exceeding $0.92 W_{\text{eff}}$, and executes a monotonic $0.5\text{ pt}$ (`sz="50"` centi-point) step-down search under `<a:noAutofit/>` and `<a:spcPct val="115000"/>` ($1.15\times$ line spacing) until $H_{\text{total}}(f) \le H_{\text{eff}}$.
2. **Closed-Form Alternating-Row Timeline Partitioner**: Enforces the exact upper-bound inequality:
   $$W_{\text{card}} \le \min\left(W_{\max},\; \left\lfloor \frac{2 W_{\text{canvas}} - g_{\min}(N - 1)}{N + 1} \times 1000 \right\rfloor \times 10^{-3}\right)$$
   At $N=6$ milestones on an $11.733''$ usable canvas, this sets $W_{\text{card}} = 3.173''$ (`cx="2901391"` EMUs), maintaining a $+0.2510''$ same-row horizontal gutter and eliminating the $-0.0668''$ ($0.0987\text{ in}^2$) AABB collision suffered by static $3.400''$ cards.
3. **Single-Axis EMU Aspect-Ratio Pinning & `@4x` Retina Assets**: Locks one primary EMU axis and derives the secondary axis from native binary pixel dimensions $(P_w, P_h)$, achieving $\le 0.0001\%$ aspect-ratio skew at $569.2–1200.0\text{ DPI}$.
4. **Pre-OpenXML Spark DLP Gate**: Deterministically scrubs confidential hourly consulting rate cards (`$495/hr`), PII emails, and API credentials before `<a:t>` XML serialization.

---

## Repository Structure

| File | Description |
| :--- | :--- |
| `slidelock_compiler.py` | Core OpenXML binary forensic inspector (`inspect_openxml_zip_invariants`), closed-form alternating-row timeline solver (`solve_alternating_timeline_card_width`), and TrueType glyph-metric solver integration. |
| `test_agent_slidelock.py` | 6-suite unit and negative-control verification suite testing all 9 invariants on compiled `.pptx` ZIP/DOM archives (`Ran 6 tests — OK`). |
| `run_slidelock_benchmark.py` | 120-deck (740 slides, 19,440 shapes) 4-iteration OpenXML ablation benchmark + live 7-model Vertex AI evaluation (`gemini-2.5-flash` through `gemini-3.8-flash` in `project="aniket-personal"`). |
| `slidelock_benchmark_results.json` | Complete empirical telemetry from the 120-deck stress audit and live Vertex AI multi-model benchmark. |
| `GOOGLE_IDF_PORTAL_SUBMISSION.md` | Complete 10-screen Google Patent / Invention Disclosure Form (`go/IDF`) with Claims 1–10, USPTO § 101 *McRO*/*Enfish* eligibility analysis, and `unzip deck.pptx` forensic detectability proof. |
| `agent_slidelock_paper.tex` | Camera-ready IEEEtran LaTeX research paper source with embedded vector `tikz` architecture diagrams and `pgfplots` quantitative charts. |
| `Agent_SlideLock_Paper.pdf` | Compiled IEEEtran camera-ready PDF generated via TeX Live 2026 `pdflatex` (`0 Errors`). |
| `plots/` | 300-DPI publication figures (`fig1_4iteration_distortion_elimination.png`, `fig2_alternating_timeline_aabb_clearance.png`, `fig3_live_gemini_35_36_37_38_multimodel_latency.png`). |

---

## Live Google Cloud Vertex AI Multi-Model Telemetry (`aniket-personal`)

| Live Vertex AI Model | Vertex LLM Latency | SlideLock Compile + 9-Invariant Audit | `<a:noAutofit/>` Tags | `<a:normAutofit/>` Tags | Max AABB Overlap | All 9 Invariants |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `gemini-2.5-flash` | `2,141.6 ms` | `1,711.6 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |
| `gemini-2.5-pro` | `2,811.7 ms` | `1,623.3 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |
| `gemini-3-flash-preview` | `1,763.4 ms` | `1,757.5 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |
| `gemini-3.5-flash` | `1,976.0 ms` | `2,050.7 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |
| `gemini-3.6-flash` | `1,472.4 ms` | `1,910.7 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |
| `gemini-3.7-flash` | `2,591.5 ms` | `2,014.2 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |
| `gemini-3.8-flash` | `3,079.2 ms` | `1,877.1 ms` | `56` | `0` | `0.0000 sq.in.` | **PASS (100%)** |

---

## Quickstart Verification

```bash
# 1. Run the 6-suite unit & negative-control test suite
python3 test_agent_slidelock.py -v

# 2. Run the 120-deck OpenXML benchmark & live 7-model Gemini evaluation
python3 run_slidelock_benchmark.py

# 3. Verify LaTeX structural and citation integrity
python3 verify_tex.py
```
