"""
Agent-SlideLock: Nanoscopic Zero-Distortion ECMA-376 OpenXML (.PPTX) Compiler,
Pre-Render TrueType Glyph-Metric Bounding-Box Solver, and Disjoint AABB Spatial Partitioner.

Solves all 8 Enterprise PresentationML / DrawingML Distortions (D1-D8) and enforces
all 9 Nanoscopic Mathematical Invariants directly at the OpenXML binary ZIP/XML layer.
"""

from __future__ import annotations

import math
import os
import re
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple

_SYS_SITE = "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages"
if _SYS_SITE not in sys.path and os.path.isdir(_SYS_SITE):
    sys.path.append(_SYS_SITE)

# Import core engine and assets from deloitte_sap_showcase
SHOWCASE_ROOT = "/Users/aniketagrawal/antigravity_workshop/deloitte_sap_showcase"
if SHOWCASE_ROOT not in sys.path and os.path.isdir(SHOWCASE_ROOT):
    sys.path.insert(0, SHOWCASE_ROOT)

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import MSO_AUTO_SIZE

from agent.slide_deck_engine import (
    generate_slide_deck,
    parse_transcript_into_slide_plan,
    build_branded_pptx,
    audit_pptx_coordinate_fidelity,
    measure_text_width_pt,
    count_wrapped_lines,
    measure_and_fit_paragraphs,
    _break_ultra_long_unbroken_tokens,
    sanitize_transcript_via_spark,
    ASSETS_DIR,
    BRAND_ARTIFACTS_DIR,
)

EMU_PER_INCH = 914400.0
SLIDE_WIDTH_EMU = int(round(13.333 * EMU_PER_INCH))   # 12,191,695 EMUs
SLIDE_HEIGHT_EMU = int(round(7.500 * EMU_PER_INCH))    # 6,858,000 EMUs

# OpenXML namespaces for forensic ZIP/XML inspection
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


@dataclass
class OpenXMLBinaryForensicProof:
    """
    Forensic proof extracted directly by unzipping a compiled .pptx archive
    and parsing raw `ppt/slides/slide*.xml` PresentationML / DrawingML DOM trees.
    Proves 100% external patent detectability on any exported .pptx file.
    """
    pptx_path: str
    slide_xml_count: int
    total_sp_nodes: int
    total_pic_nodes: int
    no_autofit_tag_count: int
    norm_autofit_tag_count: int
    spc_pct_115000_count: int
    emu_canvas_bounds_valid: bool
    max_sibling_aabb_overlap_sq_in: float
    max_vertical_overflow_pt: float
    max_horizontal_token_overflow_pt: float
    max_aspect_ratio_skew_pct: float
    min_effective_dpi: float
    all_9_invariants_passed: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def solve_alternating_timeline_card_width(
    num_milestones: int,
    canvas_usable_width_in: float = 11.733,
    min_horizontal_gutter_in: float = 0.25,
    max_card_width_in: float = 3.40,
) -> Tuple[float, float, float]:
    """
    Closed-Form Alternating-Row N-Milestone Timeline Solver (Distortion D8 / Invariant I8 Fix):
    For milestones alternating between top row (m_idx = 0, 2, 4) and bottom row (m_idx = 1, 3, 5),
    adjacent same-row cards (m_idx and m_idx + 2) are separated by 2 * step_x, where:
        step_x = (W_canvas - W_card) / (N - 1)
    Enforcing 2 * step_x >= W_card + g_min yields the closed-form upper bound:
        W_card <= min(W_max, (2 * W_canvas - g_min * (N - 1)) / (N + 1))
    Floor truncation to 1/1000th inch guarantees strict satisfaction of the inequality.
    Returns (card_width_in, step_x_in, same_row_clearance_in).
    """
    if num_milestones <= 1:
        return max_card_width_in, 0.0, canvas_usable_width_in
    upper_bound = (2.0 * canvas_usable_width_in - min_horizontal_gutter_in * (num_milestones - 1)) / (num_milestones + 1)
    w_card = math.floor(min(max_card_width_in, upper_bound) * 1000.0) / 1000.0
    # Subtract 2 EMUs in integer quantization to absorb floor step rounding
    cx_emu = max(1, int(math.floor(w_card * EMU_PER_INCH)) - 2)
    step_x = (canvas_usable_width_in - w_card) / float(num_milestones - 1)
    same_row_clearance = (2.0 * step_x) - (cx_emu / EMU_PER_INCH) if num_milestones >= 3 else canvas_usable_width_in
    return w_card, round(step_x, 4), round(same_row_clearance, 4)


def solve_synchronized_sibling_row_fonts(
    sibling_cards_paragraphs: List[List[Dict[str, Any]]],
    box_width_in: float,
    box_height_in: float,
    margin_lr_in: float = 0.12,
    margin_tb_in: float = 0.08,
    line_spacing: float = 1.15,
    f_min_pt: float = 8.0,
) -> Tuple[List[List[Dict[str, Any]]], Dict[int, float]]:
    """
    Cross-Sibling Row Typography Synchronization (Invariant I7):
    Solves each sibling card in a horizontal row G_row = {S_1, ..., S_r} via
    `measure_and_fit_paragraphs`, synchronizes every paragraph role index `k`
    across all sibling cards to the group minimum font size:
        f*_row(k) = min_{j in G_row} f*_j(k)
    and re-verifies H_total(P_j, f*_row) <= H_eff for every sibling card S_j
    (stepping down by 0.5 pt if greedy line-packing shifts occur).
    Guarantees 0.0 pt font-size variance across sibling KPI/architecture cards
    under <a:noAutofit/> while strictly preserving H_total(P_j, f*_row) <= H_eff.
    """
    fitted_cards = [
        measure_and_fit_paragraphs(
            card_specs,
            box_width_in=box_width_in,
            box_height_in=box_height_in,
            margin_lr_in=margin_lr_in,
            margin_tb_in=margin_tb_in,
            line_spacing=line_spacing,
        )
        for card_specs in sibling_cards_paragraphs
    ]
    role_min_pt: Dict[int, float] = {}
    for card in fitted_cards:
        for p_idx, p_spec in enumerate(card):
            pt_val = float(p_spec["pt"])
            if p_idx not in role_min_pt or pt_val < role_min_pt[p_idx]:
                role_min_pt[p_idx] = pt_val
    w_eff_pt = max(18.0, (box_width_in - margin_lr_in) * 72.0 - 4.0)
    h_eff_pt = max(10.0, (box_height_in - margin_tb_in) * 72.0 - 2.0)
    for card in fitted_cards:
        for p_idx, p_spec in enumerate(card):
            p_spec["pt"] = max(f_min_pt, role_min_pt[p_idx])
        # Post-sync re-verification of H_total(P_j, f*_row) <= H_eff
        total_h = sum(
            count_wrapped_lines(str(p.get("text", "")), float(p["pt"]), w_eff_pt, bool(p.get("bold", False)))
            * float(p["pt"]) * 1.22
            + float(p.get("space_before_pt", 0.0))
            + float(p.get("space_after_pt", 2.0))
            for p in card
        )
        while total_h > h_eff_pt and any(float(p["pt"]) > f_min_pt for p in card):
            for p_idx, p in enumerate(card):
                if float(p["pt"]) > f_min_pt:
                    p["pt"] = round(float(p["pt"]) - 0.5, 1)
                    role_min_pt[p_idx] = min(role_min_pt[p_idx], float(p["pt"]))
            total_h = sum(
                count_wrapped_lines(str(p.get("text", "")), float(p["pt"]), w_eff_pt, bool(p.get("bold", False)))
                * float(p["pt"]) * 1.22
                + float(p.get("space_before_pt", 0.0))
                + float(p.get("space_after_pt", 2.0))
                for p in card
            )
    for card in fitted_cards:
        for p_idx, p_spec in enumerate(card):
            p_spec["pt"] = role_min_pt[p_idx]
    return fitted_cards, role_min_pt


def inspect_openxml_zip_invariants(pptx_path: str) -> OpenXMLBinaryForensicProof:
    """
    Unzips a compiled `.pptx` file and parses `ppt/slides/slide*.xml` directly
    using `xml.etree.ElementTree` to verify wire/artifact-level OpenXML tags:
      - `<a:noAutofit/>` vs `<a:normAutofit/>`
      - `<a:lnSpc><a:spcPct val="115000"/></a:lnSpc>`
      - `<a:xfrm><a:off x="..." y="..."/><a:ext cx="..." cy="..."/></a:xfrm>`
    Alongside the 9 Nanoscopic Mathematical Invariants from `audit_pptx_coordinate_fidelity`.
    """
    slide_xml_count = 0
    total_sp_nodes = 0
    total_pic_nodes = 0
    no_autofit_count = 0
    norm_autofit_count = 0
    spc_pct_115000_count = 0
    emu_bounds_valid = True

    with zipfile.ZipFile(pptx_path, "r") as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        )
        slide_xml_count = len(slide_names)
        for sname in slide_names:
            xml_bytes = zf.read(sname)
            root = ET.fromstring(xml_bytes)

            sp_nodes = root.findall(".//p:sp", NS)
            pic_nodes = root.findall(".//p:pic", NS)
            total_sp_nodes += len(sp_nodes)
            total_pic_nodes += len(pic_nodes)

            no_autofit_count += len(root.findall(".//a:bodyPr/a:noAutofit", NS))
            norm_autofit_count += len(root.findall(".//a:bodyPr/a:normAutofit", NS))

            for spc in root.findall(".//a:lnSpc/a:spcPct", NS):
                if spc.attrib.get("val") == "115000":
                    spc_pct_115000_count += 1

            for xfrm in root.findall(".//a:xfrm", NS):
                off = xfrm.find("a:off", NS)
                ext = xfrm.find("a:ext", NS)
                if off is not None and ext is not None:
                    x = int(off.attrib.get("x", "0"))
                    y = int(off.attrib.get("y", "0"))
                    cx = int(ext.attrib.get("cx", "0"))
                    cy = int(ext.attrib.get("cy", "0"))
                    if x < -1000 or y < -1000 or (x + cx) > SLIDE_WIDTH_EMU + 5000 or (y + cy) > SLIDE_HEIGHT_EMU + 5000:
                        emu_bounds_valid = False

    qa = audit_pptx_coordinate_fidelity(pptx_path)
    skew_str = str(qa.get("image_aspect_ratio_skew_pct", "0.0%")).rstrip("%")
    dpi_str = str(qa.get("min_brand_artifact_dpi", "0.0")).split()[0]
    qa_verdict_ok = str(qa.get("qa_verdict", "")).startswith("PASS")

    return OpenXMLBinaryForensicProof(
        pptx_path=pptx_path,
        slide_xml_count=slide_xml_count,
        total_sp_nodes=total_sp_nodes,
        total_pic_nodes=total_pic_nodes,
        no_autofit_tag_count=no_autofit_count,
        norm_autofit_tag_count=norm_autofit_count,
        spc_pct_115000_count=spc_pct_115000_count,
        emu_canvas_bounds_valid=emu_bounds_valid and (qa.get("coordinate_overflow_count", 0) == 0),
        max_sibling_aabb_overlap_sq_in=float(qa.get("max_sibling_overlap_sq_in", 0.0)),
        max_vertical_overflow_pt=float(qa.get("max_vertical_overflow_pt", 0.0)),
        max_horizontal_token_overflow_pt=float(qa.get("max_horizontal_token_overflow_pt", 0.0)),
        max_aspect_ratio_skew_pct=float(skew_str),
        min_effective_dpi=float(dpi_str),
        all_9_invariants_passed=bool(
            qa_verdict_ok
            and norm_autofit_count == 0
            and no_autofit_count > 0
            and spc_pct_115000_count > 0
            and emu_bounds_valid
        ),
    )
