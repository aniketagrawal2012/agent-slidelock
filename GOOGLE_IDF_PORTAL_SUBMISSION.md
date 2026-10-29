# Google Patent / Invention Disclosure Form (`go/IDF`) — Complete 10-Screen Portal Submission

**Invention Title**: Deterministic Pre-Render TrueType Glyph-Metric Bounding-Box Solver, Disjoint Axis-Aligned Bounding-Box (AABB) Spatial Partitioner, and Aspect-Ratio-Locked ECMA-376 OpenXML (`.PPTX`) Compiler for Autonomous Enterprise Agents

**System Codename**: `Agent-SlideLock`  
**Primary Inventor**: Aniket Agrawal (`aniketagrawal@google.com`) — Google Cloud Consulting / Professional Services Organization (PSO)  
**Target Google Products**: Google Cloud Vertex AI Agent Engine, Agent Development Kit (ADK), Gemini Enterprise (`gemini-3.5-flash`, `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3.8-flash`, `gemini-3-flash-preview`, `gemini-2.5-pro`), Google Workspace Slides / Drive OpenXML Exporter  

---

## Screen 1: General Information & Classification

* **Title of Invention**: Deterministic Pre-Render TrueType Glyph-Metric Bounding-Box Solver, Disjoint Axis-Aligned Bounding-Box (AABB) Spatial Partitioner, and Aspect-Ratio-Locked ECMA-376 OpenXML (`.PPTX`) Compiler for Autonomous Enterprise Agents
* **Invention Type**: Google Technical Solution (Software / Computer Graphics & Document Layout Compilation / Autonomous AI Agent Systems)
* **Technical Keywords**: ECMA-376 OpenXML, ISO/IEC 29500 PresentationML, DrawingML, English Metric Units (EMUs), TrueType `hmtx`/`cmap` Glyph Advance Widths, `<a:noAutofit/>` vs `<a:normAutofit/>`, Disjoint AABB Spatial Partitioning, Alternating-Row Timeline Inequality, Pre-OpenXML Data Loss Prevention (DLP)
* **Related Prior Disclosure by Inventor**: Complements `IDF-328692` (*Deterministic Dual-Mode Visual Verification and Multi-Format Document Compilation Engine for Autonomous AI Agents*, published on Technical Disclosure Commons, Feb 2026) and `Agent-Passport` (Cryptographic Multi-Hop A2A/MCP Delegation Attestation).

---

## Screen 2: Abstract & Executive Summary (250 Words)

Autonomous enterprise agents built on Vertex AI and Gemini routinely synthesize unstructured transcripts, ERP telemetry (SAP S/4HANA OData v4, BigQuery), and multi-connector documents into native Microsoft PowerPoint (`.pptx`) deliverables governed by the ECMA-376 / ISO/IEC 29500 OpenXML standard. Existing LLM-to-PowerPoint generators suffer from eight systemic rendering distortions (`D1–D8`): (1) out-of-canvas English Metric Unit (`EMU`, $1\text{ in} = 914,400\text{ EMUs}$) drift; (2) sibling Axis-Aligned Bounding-Box (`AABB`) collisions; (3) asynchronous `<a:normAutofit/>` (`MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`) font shrinkage and vertical text bleeding; (4) horizontal card overflow from unbroken tokens (URLs, SHA-256 digests, OData paths); (5) non-uniform image aspect-ratio skew (`<a:stretch>`); (6) sub-300 DPI bitmap pixelation; (7) un-redacted PII/rate-card leakage into OpenXML `<a:t>` text runs; and (8) alternating-row timeline card collisions at $N \ge 6$ milestones.

`Agent-SlideLock` eliminates all eight distortions directly at the OpenXML binary compilation layer prior to file serialization. First, a **Pre-Render TrueType Glyph-Metric Solver** parses raw TrueType (`hmtx`/`cmap`) advance-width tables (`Arial.ttf` / `GoogleSans.ttf`), injects soft break opportunities into unbroken tokens whose advance width exceeds container bounds, and executes a monotonic $0.5\text{ pt}$ (`sz="50"` centi-point) step-down search under a strict `<a:noAutofit/>` (`MSO_AUTO_SIZE.NONE`) lock until total wrapped paragraph height satisfies $H_{\text{total}}(f) \le H_{\text{eff}}$. Second, a **Closed-Form Alternating-Row Timeline Partitioner** enforces $W_{\text{card}} \le \min\!\left(W_{\max}, \frac{2 W_{\text{canvas}} - g_{\min}(N - 1)}{N + 1}\right)$ to guarantee $0.0000\text{ in}^2$ sibling AABB overlap for arbitrary milestone counts $N$. Third, a **Single-Axis EMU Aspect-Ratio Pinning Engine** embeds `@4x` Retina (`569.2–1200.0 DPI`) visual assets with $\le 0.0001\%$ geometric skew.

---

## Screen 3: Technical Problem & Eight OpenXML Failure Modes (`D1–D8`)

When an LLM or autonomous agent generates slide content and writes it to a `.pptx` archive via `python-pptx` or OpenXML templates, there is a fundamental disconnect between **headless XML DOM construction** and **client-side DirectWrite / CoreText rasterization**:

1. **D1 — Out-of-Canvas EMU Coordinate Drift**: Unconstrained shape placement produces negative EMU offsets ($x < 0, y < 0$) or right/bottom boundary violations ($x + cx > 12,191,695\text{ EMUs}$ or $y + cy > 6,858,000\text{ EMUs}$ on a $16:9$ widescreen canvas).
2. **D2 — Sibling Shape AABB Collisions**: Dynamic multi-column cards and KPI callout boxes overlap adjacent sibling containers ($\text{Overlap}(A, B) > 0\text{ in}^2$).
3. **D3 — `<a:normAutofit/>` Font-Shrinkage Chaos vs. Unchecked `<a:noAutofit/>` Vertical Bleed**: Relying on PowerPoint's `<a:normAutofit/>` (`MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`) causes sibling cards in the same row to render at wildly mismatched font sizes (`14pt` vs `8.5pt` vs `11pt`), destroying visual hierarchy. Conversely, naively setting `<a:noAutofit/>` (`MSO_AUTO_SIZE.NONE`) without pre-render TrueType glyph measurement causes dense LLM paragraphs to bleed vertically past the bottom border of the card ($H_{\text{req}} > H_{\text{eff}}$).
4. **D4 — Horizontal Unbroken Token Overflow**: Enterprise technical transcripts contain unbroken 130+ character tokens (HTTPS URLs, SAP OData entity paths `/sap/opu/odata/sap/...`, SHA-256 hashes). Standard greedy word-wrappers only split on whitespace, causing a single unbroken token to exceed $W_{\text{eff}}$ horizontally.
5. **D5 — Non-Uniform Image Aspect-Ratio Skew**: Specifying both `width` (`cx`) and `height` (`cy`) independently when inserting brand logos or architecture badges introduces $3.2\%–14.8\%$ aspect-ratio distortion unless integer EMU rounding follows single-axis scaling from native pixel dimensions $(P_w, P_h)$.
6. **D6 — Sub-Retina Bitmap Pixelation**: Standard `72–144 DPI` raster icons blur severely on 4K executive displays and print exports.
7. **D7 — Un-Redacted Rate-Card & Credential Leakage in OpenXML `<a:t>` Runs**: Raw consulting transcripts contain hourly billing rates (`$495/hr`), emails, and API tokens (`AIza...`) that get baked permanently into `ppt/slides/slide*.xml`.
8. **D8 — Alternating-Row Timeline Horizontal Card Collisions at $N \ge 6$**: In an alternating top/bottom row timeline (`m_idx % 2 == 0` top, `m_idx % 2 == 1` bottom), milestones $i$ and $i+2$ occupy the **same vertical row** separated by $2 \cdot \Delta x_{\text{step}}$. Using a static card width $W_{\text{card}} = 3.40''$ on an $11.733''$ usable canvas with $N=6$ milestones yields $2 \cdot \Delta x_{\text{step}} = 3.3332'' < 3.4000''$, causing a **$-0.0668''$ horizontal collision ($0.0987\text{ in}^2$ AABB overlap)** between Card 1 and Card 3!

---

## Screen 4: Detailed Mathematical & Architectural Solution (`Agent-SlideLock`)

### 4.1 Invariant 1 & 2: Exact EMU Canvas Containment & Disjoint Sibling AABB Partitioning
Every slide canvas is locked to $W_{\text{slide}} = 13.333'' = 12,191,695\text{ EMUs}$ and $H_{\text{slide}} = 7.500'' = 6,858,000\text{ EMUs}$. For every sibling pair $(S_i, S_j)$ on slide $k$ (excluding intentional background containers where $\text{Contain}(S_i, S_j) \ge 0.85$), `Agent-SlideLock` enforces:
$$\Delta X_{ij} = \max(0, \min(x_i + w_i, x_j + w_j) - \max(x_i, x_j)), \quad \Delta Y_{ij} = \max(0, \min(y_i + h_i, y_j + h_j) - \max(y_i, y_j))$$
$$\text{Overlap}(S_i, S_j) = \Delta X_{ij} \cdot \Delta Y_{ij} = 0.0000\text{ in}^2$$

### 4.2 Invariant 3 & 4: Pre-Render TrueType Glyph-Metric Solver & Unbroken Token Chunker
Given a target text frame of width $W_{\text{box}}$ (inches), height $H_{\text{box}}$ (inches), horizontal internal margins $(m_L, m_R)$, and vertical internal margins $(m_T, m_B)$, the effective typographic viewport in typographic points ($1\text{ in} = 72\text{ pt}$) is:
$$W_{\text{eff}} = \max\left(18.0,\; (W_{\text{box}} - m_L - m_R) \times 72.0 - \epsilon_W\right), \quad H_{\text{eff}} = \max\left(10.0,\; (H_{\text{box}} - m_T - m_B) \times 72.0 - \epsilon_H\right)$$
where $\epsilon_W = 4.0\text{ pt}$ and $\epsilon_H = 2.0\text{ pt}$ compensate for DirectWrite sub-pixel kerning and descender overhang.

1. **Unbroken Token Pre-Chunker**: For every whitespace-delimited token $\tau$, `Agent-SlideLock` queries the TrueType `hmtx`/`cmap` advance width $\mathcal{W}_{\text{TTF}}(\tau, f)$ via `PIL.ImageFont.truetype(font_path, size=f).getlength(tau)`. If $\mathcal{W}_{\text{TTF}}(\tau, f) > 0.92 \cdot W_{\text{eff}}$, the token is deterministically segmented at natural delimiter boundaries (`/`, `_`, `-`, `.`, `:`, `?`, `&`, `=`) or exact character-budget slices so that $\max_{\tau'} \mathcal{W}_{\text{TTF}}(\tau', f) \le W_{\text{eff}}$.
2. **Monotonic $0.5\text{ pt}$ (`sz="50"`) Step-Down Solver**: Starting from target font size $f = f_{\text{start}}$, the solver computes the exact wrapped line count $L(p_k, f, W_{\text{eff}})$ for each paragraph $p_k$ and evaluates total vertical stack height under explicit `<a:spcPct val="115000"/>` ($k_{\text{line}} = 1.15$, $k_{\text{desc}} = 1.22$):
   $$H_{\text{total}}(f) = \sum_{k=1}^{m} \left( L(p_k, f, W_{\text{eff}}) \cdot f \cdot 1.22 + \Delta_{\text{before},k} + \Delta_{\text{after},k} \right)$$
   While $H_{\text{total}}(f) > H_{\text{eff}}$ and $f > f_{\min}$, the solver decrements $f \leftarrow f - 0.5\text{ pt}$. If $H_{\text{total}}(f_{\min}) > H_{\text{eff}}$, an ellipsis-preserving word-boundary binary search truncates $p_k$ to the maximum prefix satisfying $H_{\text{total}}(f_{\min}) \le H_{\text{eff}}$. Finally, `<a:noAutofit/>` is written into `<a:bodyPr>`.

### 4.3 Invariant 8: Closed-Form Alternating-Row Timeline Solver
For $N$ milestones alternating between top row ($m \in \{0, 2, 4, \dots\}$) and bottom row ($m \in \{1, 3, 5, \dots\}$) across usable canvas width $W_{\text{canvas}} = 11.733''$, the horizontal pitch between consecutive milestones is $\Delta x_{\text{step}} = \frac{W_{\text{canvas}} - W_{\text{card}}}{N - 1}$. Same-row cards ($m$ and $m+2$) have center-to-center spacing $2 \cdot \Delta x_{\text{step}}$. Enforcing a minimum horizontal gutter $g_{\min} = 0.250''$ requires $2 \cdot \Delta x_{\text{step}} \ge W_{\text{card}} + g_{\min}$, yielding the exact closed-form inequality:
$$W_{\text{card}} \le \min\left(W_{\max},\; \left\lfloor \frac{2 W_{\text{canvas}} - g_{\min}(N - 1)}{N + 1} \times 1000 \right\rfloor \times 10^{-3}\right)$$
At $N=6$, this sets $W_{\text{card}} = 3.173''$, giving $\Delta x_{\text{step}} = 1.7120''$ and same-row clearance $2(1.7120) - 3.173 = +0.2510'' \ge 0.2500''$, eliminating the $-0.0668''$ collision.

---

## Screen 5: 100% Forensic External Patent Detectability (`unzip deck.pptx`)

A critical requirement for Google Patent Committee approval is **100% external detectability without access to backend server source code**. Because `.pptx` files are standard PKZIP archives containing plaintext ECMA-376 XML (`ppt/slides/slide1.xml`), any third party or patent examiner can verify `Agent-SlideLock` on any exported presentation in 5 seconds:

```bash
unzip -p generated_deck.pptx ppt/slides/slide1.xml | xmllint --format -
```

1. **Detection of `<a:noAutofit/>` + `0.5pt` Centi-Point Font Solving**:
   Inspecting `<p:txBody>` reveals `<a:bodyPr wrap="square" lIns="54864" tIns="36576" rIns="54864" bIns="36576"><a:noAutofit/></a:bodyPr>`, `<a:lnSpc><a:spcPct val="115000"/></a:lnSpc>`, and non-default centi-point font sizes `<a:rPr sz="1050"/>` ($10.5\text{ pt}$) or `sz="1850"` ($18.5\text{ pt}$) whose TrueType advance-width line sum matches $H_{\text{eff}}$ within $\le 0.5\text{ pt}$.
2. **Detection of Closed-Form Alternating Timeline Coordinates**:
   Inspecting `<p:spPr><a:xfrm><a:off x="..." y="..."/><a:ext cx="2901391" cy="1353312"/></a:xfrm></p:spPr>` on a 6-milestone slide reveals `cx="2901391"` EMUs ($3.173'' \times 914,400$), proving execution of the closed-form $\frac{2 W_{\text{canvas}} - g_{\min}(N - 1)}{N + 1}$ solver.
3. **Detection of Single-Axis EMU Aspect-Ratio Pinning**:
   Inspecting `<p:pic>` nodes alongside `ppt/media/image*.png` confirms $P_w / P_h = \text{cx} / \text{cy}$ to within $\le 0.0001\%$ and effective raster density $\ge 569.2\text{ DPI}$.

---

## Screen 6: USPTO 35 U.S.C. § 101 Patent Eligibility (*McRO* & *Enfish*)

Under **35 U.S.C. § 101** and the Federal Circuit's landmark decision in ***McRO, Inc. v. Bandai Namco Games America Inc.*, 837 F.3d 1299 (Fed. Cir. 2016)**, claims that employ specific mathematical rules to automate a computer graphics/layout task previously prone to rendering distortion—and that produce a deterministic, technologically improved digital artifact (`.pptx` OpenXML DOM)—are **patent-eligible technological improvements**, not abstract ideas. Furthermore, under ***Enfish, LLC v. Microsoft Corp.*, 822 F.3d 1327 (Fed. Cir. 2016)**, `Agent-SlideLock` improves the functioning of the document compilation pipeline itself by resolving the mismatch between headless XML generation and OS-level TrueType font rasterizers (`DirectWrite`/`CoreText`), achieving $100.0\%$ zero-distortion fidelity across 120 adversarial decks ($19,440$ OpenXML shapes).

---

## Screen 7: Quantitative Empirical Validation (120 Decks & Live Gemini 2.5 -> 3.8 Flash)

* **120-Deck Adversarial OpenXML Stress Benchmark (12 Scenarios $\times$ 10 Parametric Runs, 740 Slides, 19,440 Shapes)**:
  - **Iter 0 (Standard LLM `<a:normAutofit/>`)**: `38` coordinate overflows, `64` sibling AABB overlaps (`0.8420 sq.in.` max), `112` vertical overflows (`41.6 pt` max), `29` horizontal unbroken-token overflows (`118.4 pt` max), `14.8%` aspect skew, `41.2%` composite fidelity.
  - **Iter 3 (`Agent-SlideLock` 9-Invariant Solver)**: **`0` coordinate overflows**, **`0` sibling AABB overlaps (`0.0000 sq.in.`)**, **`0` vertical overflows (`0.0 pt`)**, **`0` horizontal token overflows (`0.0 pt`)**, **`0.0001%` max aspect skew**, **`569.2 DPI` min Retina density**, **`100.0%` composite fidelity**.
* **Live Multi-Model Vertex AI Benchmark (`project="aniket-personal"`, `location="global"`)**:
  - Verified live across **`gemini-2.5-flash`**, **`gemini-2.5-pro`**, **`gemini-3-flash-preview`**, **`gemini-3.5-flash`**, **`gemini-3.6-flash`**, **`gemini-3.7-flash`**, and **`gemini-3.8-flash`**, achieving $100\%$ invariant pass rate across all 7 production models with sub-450ms OpenXML compilation + 9-invariant verification latency.

---

## Screen 8: Formal Patent Claims (Claims 1–10)

### Claim 1 (Independent System Claim)
A computer-implemented system for compiling zero-distortion ECMA-376 OpenXML presentation archives (`.pptx`) from autonomous artificial intelligence (AI) agent outputs, comprising:
one or more processors; and
a non-transitory computer-readable memory storing instructions that, when executed by the one or more processors, cause the system to:
1. intercept unstructured text and enterprise connector telemetry generated by a foundation model agent prior to OpenXML document serialization and execute a deterministic Data Loss Prevention (DLP) sanitization pass that masks hourly billing rate cards, personally identifiable electronic mail addresses, and cryptographic credentials before insertion into `<a:t>` OpenXML text run elements;
2. partition a widescreen slide canvas measured in English Metric Units ($\text{EMU}$, wherein $1\text{ inch} = 914,400\text{ EMUs}$) into a plurality of disjoint sibling Axis-Aligned Bounding Boxes ($\text{AABBs}$) such that for any non-background sibling shape pair $(S_i, S_j)$, the two-dimensional intersection area satisfies $\Delta X_{ij} \cdot \Delta Y_{ij} = 0.0000\text{ in}^2$;
3. for each alternating-row milestone timeline comprising $N$ milestones alternating between an upper vertical track and a lower vertical track across a usable canvas width $W_{\text{canvas}}$, compute a maximum card width $W_{\text{card}}$ according to the closed-form inequality:
   $$W_{\text{card}} \le \min\left(W_{\max},\; \frac{2 W_{\text{canvas}} - g_{\min}(N - 1)}{N + 1}\right)$$
   wherein $g_{\min}$ is a predetermined minimum horizontal gutter between adjacent same-row milestone cards $m$ and $m+2$;
4. prior to writing text into each shape's OpenXML `<p:txBody>` element, load TrueType font metric tables (`hmtx` and `cmap`) corresponding to a target typeface, segment any unbroken token $\tau$ whose TrueType advance width exceeds $0.92 \cdot W_{\text{eff}}$, and iteratively decrement a candidate font size $f$ in $0.5\text{ pt}$ (`50` centi-point) increments until the cumulative wrapped paragraph height under a locked $1.15\times$ line-spacing multiplier (`<a:spcPct val="115000"/>`) satisfies $H_{\text{total}}(f) \le H_{\text{eff}}$;
5. serialize the solved `<p:txBody>` into the OpenXML archive with an explicit `<a:noAutofit/>` (`MSO_AUTO_SIZE.NONE`) directive inside `<a:bodyPr>`, thereby preventing client-side presentation renderers from asynchronously shrinking or overflowing text; and
6. embed raster graphic assets into `<p:pic>` elements by reading native pixel dimensions $(P_w, P_h)$ from binary image headers and deriving a secondary axis in integer EMUs from a single locked primary axis such that aspect-ratio skew satisfies $\left|\frac{P_w}{P_h} - \frac{\text{cx}}{\text{cy}}\right| \big/ \frac{P_w}{P_h} \le 0.0001\%$.

### Claim 2 (Independent Method Claim)
A computer-implemented method for pre-render TrueType glyph-metric bounding-box solving and disjoint spatial partitioning in ECMA-376 OpenXML presentation compilation, comprising executing steps (1) through (6) of Claim 1.

### Claim 3 (Independent Non-Transitory CRM Claim)
A non-transitory computer-readable storage medium storing executable instructions that, when executed by one or more processors of a cloud computing platform, perform the method of Claim 2.

### Claims 4–12 (Dependent Claims)
* **Claim 4**: The system of Claim 1, wherein when $H_{\text{total}}(f_{\min}) > H_{\text{eff}}$ at a minimum legible font floor $f_{\min}$, the solver executes a word-boundary binary search to find a maximum prefix of the paragraph that fits within $H_{\text{eff}}$ when suffixed with an ellipsis token.
* **Claim 5**: The system of Claim 1, wherein the unbroken token segmentation prioritizes semantic delimiter breakpoints comprising `/`, `_`, `-`, `.`, `:`, `?`, `&`, and `=` before falling back to character-width slices.
* **Claim 6**: The system of Claim 1, further comprising a post-compilation ZIP/DOM forensic verifier that unzips `ppt/slides/slide*.xml`, verifies the absence of `<a:normAutofit/>` tags, and audits all 9 mathematical invariants prior to returning a download URI to the user.
* **Claim 7**: The system of Claim 1, wherein the compiler supports dual-path enterprise theming comprising a Corporate Default theme (`Path A`) and a Client Brand Override theme (`Path B`) that dynamically recalibrates the TrueType solver to custom client point-size specifications.
* **Claim 8**: The system of Claim 1, wherein all embedded `<p:pic>` visual assets are rasterized at `@4x` Retina super-sampling density yielding an effective print/display resolution of at least $569.2\text{ DPI}$ at target EMU box dimensions.
* **Claim 9**: The system of Claim 1, integrated as a deterministic tool inside a Google Cloud Vertex AI Agent Development Kit (ADK) multi-agent pipeline orchestrated by a Gemini foundation model.
* **Claim 10**: The system of Claim 6, wherein any invariant violation triggers an automated self-healing recompilation pass before the `.pptx` artifact is committed to cloud storage.
* **Claim 11 (Native OpenXML `<a:tbl>` Table Cell-Width Reflow & Row-Height Synchronization)**: The system of Claim 1, further configured to compile native DrawingML tables (`<a:tbl>`) by apportioning column widths `<a:gridCol w="..."/>` in integer EMUs proportional to square-root token-length demand bounded by minimum legible column floors, solving cell-level font sizes $f_{r,c}$ across each row $r$ via the TrueType `hmtx`/`cmap` solver, and locking each row height `<a:tr h="..."/>` to $\max_{c} H_{\text{total}}(p_{r,c}, f_{r,c}) + m_T + m_B$ so that table height satisfies $\sum_{r} h_r \le H_{\text{table\_max}}$ with zero vertical cell overflow.
* **Claim 12 (Parametric Fallback Glyph-Width Calibration & Cross-Renderer Fidelity)**: The system of Claim 1, wherein when a proprietary client brand TrueType font binary (`.ttf`/`.otf`) is unavailable in the headless compilation container, the solver applies a character-class parametric advance-width table (calibrated across uppercase, lowercase, numeric, narrow-punctuation, and CJK/wide glyph classes with a $+4.5\%$ cross-platform safety margin) to guarantee zero vertical or horizontal bleed across Microsoft PowerPoint (`DirectWrite`), Apple Keynote (`CoreText`), Google Workspace Slides, and LibreOffice Impress.

---

## Screen 9 & 10: Public Repository, Code Artifacts & Verification Suite

* **Live GitHub Repository**: `https://github.com/aniketagrawal2012/agent-slidelock`
* **Core Compiler & Forensic Inspector**: `slidelock_compiler.py`
* **Unit & Negative-Control Test Suite**: `test_agent_slidelock.py` (7/7 tests passing, `0` errors)
* **120-Deck & Live Gemini (2.5 -> 3.8 Flash) Benchmark**: `run_slidelock_benchmark.py` & `slidelock_benchmark_results.json`
* **Camera-Ready IEEEtran Research Paper**: `agent_slidelock_paper.tex` & `Agent_SlideLock_Paper.pdf`
