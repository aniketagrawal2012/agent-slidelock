"""
Comprehensive Unit & Extreme Edge-Case Test Suite for Agent-SlideLock.

Verifies all 9 Nanoscopic Mathematical Invariants and 8 Distortions (D1-D8)
directly at the ECMA-376 OpenXML binary ZIP/DOM (`ppt/slides/slide*.xml`) level.
"""

import os
import tempfile
import unittest

from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.util import Inches, Pt

from slidelock_compiler import (
    solve_alternating_timeline_card_width,
    solve_synchronized_sibling_row_fonts,
    inspect_openxml_zip_invariants,
    measure_text_width_pt,
    count_wrapped_lines,
    measure_and_fit_paragraphs,
    _break_ultra_long_unbroken_tokens,
    sanitize_transcript_via_spark,
    generate_slide_deck,
    parse_transcript_into_slide_plan,
    build_branded_pptx,
)


class TestAgentSlideLockInvariants(unittest.TestCase):
    def test_invariant_1_and_2_openxml_binary_dom_and_disjoint_aabb(self):
        """Verifies <a:noAutofit/>, <a:spcPct val='115000'/>, and 0.0000 sq.in. AABB overlap in raw XML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pptx = os.path.join(tmpdir, "test_deloitte_default.pptx")
            res = generate_slide_deck(
                transcript_or_notes=(
                    "Deloitte Consulting Scrapbook Weekly Status: 6 Priority Agents evaluated on Gemini 3.8 Flash. "
                    "Lead Partner billed at $495/hr, contact aniketagrawal@google.com. "
                    "Phase 1: Enforce MSO_AUTO_SIZE.NONE and @4x Retina icon pinning. "
                    "Phase 2: Zero-distortion native OpenXML .pptx compilation."
                ),
                deck_title="Deloitte Consulting Scrapbook Weekly Status",
                theme="deloitte_default",
                output_filename=out_pptx,
            )
            proof = inspect_openxml_zip_invariants(res["pptx_path"])
            self.assertEqual(proof.slide_xml_count, 6)
            self.assertEqual(proof.norm_autofit_tag_count, 0)
            self.assertGreaterEqual(proof.no_autofit_tag_count, 56)
            self.assertGreaterEqual(proof.spc_pct_115000_count, 110)
            self.assertTrue(proof.emu_canvas_bounds_valid)
            self.assertEqual(proof.max_sibling_aabb_overlap_sq_in, 0.0)
            self.assertEqual(proof.max_vertical_overflow_pt, 0.0)
            self.assertEqual(proof.max_horizontal_token_overflow_pt, 0.0)
            self.assertLessEqual(proof.max_aspect_ratio_skew_pct, 0.0001)
            self.assertGreaterEqual(proof.min_effective_dpi, 569.0)
            self.assertTrue(proof.all_9_invariants_passed)

    def test_invariant_3_and_4_adversarial_145char_title_and_130char_unbroken_token(self):
        """Verifies Pre-Render TrueType Glyph Solver on 145-char titles and 130-char unbroken URLs/hashes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pptx = os.path.join(tmpdir, "test_adversarial_tokens.pptx")
            unbroken_url = (
                "https://sap-s4hana-netweaver-gateway-prod-us-central1.corporate.deloitte.com/"
                "sap/opu/odata/sap/API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice"
            )
            sha_digest = "SHA256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
            long_title = (
                "Global Multi-Region SAP S/4HANA Finance Transformation, Autonomous FastMCP Governance, "
                "and Zero-Distortion Executive Presentation Architecture"
            )
            res = generate_slide_deck(
                transcript_or_notes=f"Endpoint {unbroken_url} verified with digest {sha_digest} and [CONFIDENTIAL_HOURLY_RATE_MASKED].",
                deck_title=long_title,
                theme="client_override",
                output_filename=out_pptx,
            )
            proof = inspect_openxml_zip_invariants(res["pptx_path"])
            self.assertEqual(proof.max_vertical_overflow_pt, 0.0)
            self.assertEqual(proof.max_horizontal_token_overflow_pt, 0.0)
            self.assertTrue(proof.all_9_invariants_passed)

    def test_invariant_8_closed_form_alternating_timeline_solver_all_n(self):
        """Verifies closed-form alternating-row timeline inequality for all N in {1..8}."""
        for n in range(1, 9):
            w_card, step_x, clearance = solve_alternating_timeline_card_width(
                num_milestones=n, canvas_usable_width_in=11.733, min_horizontal_gutter_in=0.25, max_card_width_in=3.40
            )
            if n >= 3:
                self.assertGreaterEqual(clearance, 0.250, f"Failed min gutter for N={n}: clearance={clearance}")
            if n == 6:
                self.assertAlmostEqual(w_card, 3.173, places=3)

        # Also compile a full 6-milestone (N=6) deck and verify 0.0000 sq.in. AABB overlap
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pptx = os.path.join(tmpdir, "test_n6_timeline.pptx")
            plan = parse_transcript_into_slide_plan("Testing N=6 alternating timeline geometry.", "Six-Phase Timeline", target_slides=6)
            plan["slides"][4]["milestones"] = [
                {"phase": f"Week {i} • GATE 0{i}", "title": f"Gate {i}: Milestone", "desc": "Zero AABB collision across alternating rows."}
                for i in range(1, 7)
            ]
            build_branded_pptx(plan, out_pptx, theme="deloitte_default")
            proof = inspect_openxml_zip_invariants(out_pptx)
            self.assertEqual(proof.max_sibling_aabb_overlap_sq_in, 0.0)
            self.assertTrue(proof.all_9_invariants_passed)

    def test_invariant_9_spark_dlp_pre_openxml_sanitization(self):
        """Verifies deterministic masking of $/hr rate cards, PII emails, and API keys."""
        fake_key = "AIza" + "SySyntheticTestKey1234567890"
        raw = f"Managing Director rate is $525/hr, email lead_architect@deloitte.com, key {fake_key}."
        sanitized = sanitize_transcript_via_spark(raw)
        cleaned = sanitized["sanitized_text"]
        self.assertNotIn("$525/hr", cleaned)
        self.assertNotIn("lead_architect@deloitte.com", cleaned)
        self.assertNotIn(fake_key, cleaned)
        self.assertGreaterEqual(sanitized["sanitization_telemetry"]["rate_cards_masked"], 1)
        self.assertGreaterEqual(sanitized["sanitization_telemetry"]["emails_masked"], 1)
        self.assertGreaterEqual(sanitized["sanitization_telemetry"]["tokens_masked"], 1)

    def test_multi_connector_and_unicode_edge_cases(self):
        """Verifies SharePoint/Drive/Confluence connector ingestion + Unicode mathematical & currency glyphs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pptx = os.path.join(tmpdir, "test_connectors_unicode.pptx")
            res = generate_slide_deck(
                transcript_or_notes=(
                    "Mathematical invariants: ∀ S_i ∈ Slide, ∑(h_j) ≤ H_eff, ∆W = 0.0000 sq.in., "
                    "budget €4.2M / £3.6M / ¥620M, billing $480 per hour, secret-key-9876543210abcdef."
                ),
                deck_title="Multi-Connector & Unicode Glyph Stress Audit",
                data_connector_query="sharepoint_docs",
                theme="deloitte_default",
                output_filename=out_pptx,
            )
            proof = inspect_openxml_zip_invariants(res["pptx_path"])
            self.assertTrue(proof.all_9_invariants_passed)

    def test_negative_control_detects_distorted_naive_pptx(self):
        """Proves that inspect_openxml_zip_invariants catches <a:normAutofit/> and sibling AABB overlaps."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_pptx = os.path.join(tmpdir, "naive_distorted.pptx")
            prs = Presentation()
            prs.slide_width = Inches(13.333)
            prs.slide_height = Inches(7.5)
            slide = prs.slides.add_slide(prs.slide_layouts[6])

            # Add two overlapping sibling boxes and enable TEXT_TO_FIT_SHAPE (<a:normAutofit/>)
            tb1 = slide.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(4.0), Inches(1.0))
            tb1.text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            tb1.text_frame.text = "Overlapping sibling card 1 with normAutofit distortion."

            tb2 = slide.shapes.add_textbox(Inches(3.0), Inches(1.2), Inches(4.0), Inches(1.0))
            tb2.text_frame.text = "Overlapping sibling card 2 colliding by 2.0 x 0.8 = 1.6 sq.in."

            prs.save(bad_pptx)
            proof = inspect_openxml_zip_invariants(bad_pptx)
            self.assertGreater(proof.norm_autofit_tag_count, 0)
            self.assertGreater(proof.max_sibling_aabb_overlap_sq_in, 1.0)
            self.assertFalse(proof.all_9_invariants_passed)

    def test_invariant_7_sibling_row_font_synchronization(self):
        """Verifies that 3 sibling KPI cards with varying verbosity synchronize to identical locked font sizes."""
        cards = [
            [{"text": "Card 1 Title", "pt": 13.0, "bold": True}, {"text": "Concise bullet.", "pt": 10.5, "bold": False}],
            [{"text": "Card 2 Longer Title", "pt": 13.0, "bold": True}, {"text": "Medium length consulting bullet point for card two.", "pt": 10.5, "bold": False}],
            [
                {"text": "Card 3 Dense Enterprise Architecture Header", "pt": 13.0, "bold": True},
                {
                    "text": (
                        "Very dense multi-clause SAP S/4HANA OData v4 and FastMCP integration bullet "
                        "requiring 0.5pt step-down font calibration across the sibling row."
                    ),
                    "pt": 10.5,
                    "bold": False,
                },
            ],
        ]
        synced, role_min = solve_synchronized_sibling_row_fonts(cards, box_width_in=2.6, box_height_in=0.95)
        self.assertEqual(synced[0][0]["pt"], synced[1][0]["pt"])
        self.assertEqual(synced[1][0]["pt"], synced[2][0]["pt"])
        self.assertEqual(synced[0][1]["pt"], synced[1][1]["pt"])
        self.assertEqual(synced[1][1]["pt"], synced[2][1]["pt"])
        self.assertLessEqual(role_min[1], 10.5)


if __name__ == "__main__":
    unittest.main()
