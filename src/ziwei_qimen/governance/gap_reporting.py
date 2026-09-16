from enum import Enum


class GapType(Enum):
    UNDOCUMENTED = "undocumented"
    SOURCE_CONFLICT = "source_conflict"
    INSUFFICIENT_INPUT = "insufficient_input"
    UNCERTAIN_HOUR = "uncertain_hour"


GAP_PRESENTATION_RULES = {
    GapType.UNDOCUMENTED: {
        "format": "\u539f\u6587\u672a\u8f09",
        "forbidden": ["fabricate_original_text", "fabricate_juan_or_pian", "fabricate_item_count", "disguise_mainstream_as_original"],
    },
    GapType.SOURCE_CONFLICT: {
        "format": "list_both_filenames_or_juan_numbers_and_literal_text_then_ask_user",
        "forbidden": ["auto_select_one_side", "auto_reconcile", "enter_halt_flow"],
    },
    GapType.INSUFFICIENT_INPUT: {
        "format": "state_missing_item_current_precision_level_and_affected_conclusions",
        "forbidden": ["assume_default_hour", "assume_default_coordinates", "silent_approximation"],
    },
    GapType.UNCERTAIN_HOUR: {
        "format": "list_all_candidate_charts_with_comparison_table_and_split_common_and_divergent_conclusions",
        "forbidden": ["output_single_chart_only", "average_candidates", "pick_most_likely"],
    },
}

CANDIDATE_CHART_OUTPUT_RULES = [
    "each_candidate_hour_coordinate_or_date_produces_one_full_chart",
    "no_chart_may_be_simplified_or_summarized",
    "comparison_table_lists_basis_and_key_divergent_fields",
    "unanimous_conclusions_marked_as_such",
    "divergent_conclusions_all_retained_without_arbitration",
    "external_evidence_narrowing_must_disclose_evidence_and_reasoning_and_keep_excluded_candidates_in_appendix",
]

CONFIDENCE_LEVELS = ["precise", "hour_range", "date_only", "location_unknown"]
