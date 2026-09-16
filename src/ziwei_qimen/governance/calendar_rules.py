TRUE_SOLAR_TIME_CORRECTION_ORDER = ["daylight_saving_offset", "longitude_time_difference", "equation_of_time"]

LONGITUDE_TIME_DIFFERENCE_FORMULA = "(local_longitude - timezone_central_meridian) * 4_minutes_per_degree"

ZIWEI_LATE_ZI_HOUR = {
    "range_23_00_to_23_59_59": {
        "date_shift": "next_day",
        "day_pillar_shift": "next_day",
        "chart_output": "single_chart_only",
    },
    "range_00_00_to_00_59_59": {
        "date_shift": "none",
        "day_pillar_shift": "none",
    },
}

QIMEN_NIGHT_ZI_HOUR = {
    "range_23_00_to_23_59_59": {
        "day_pillar_shift": "none",
        "hour_pillar_shift": "next_day_zi",
        "dependent_derivations": ["xunshou", "dunyi", "zhifu", "zhishi", "xunkong", "yima"],
        "wubuyushi_reference": "current_day_stem_with_next_day_zi_hour_stem",
    },
    "range_00_00_to_00_59_59": {
        "day_pillar_shift": "none",
        "hour_pillar_shift": "none",
    },
}

ZI_HOUR_RULE_CROSS_USE_FORBIDDEN = True

LEAP_MONTH_EFFECTIVE_RULE = {
    "applies_to": "birth_month_is_leap_month_only",
    "day_1_to_15": "original_month",
    "day_16_to_end_including_29_30": "next_month",
}

SOLAR_CALENDAR_LUNAR_CALENDAR_CROSS_CHECK = "true_solar_time_day_boundary_is_authoritative"

QIMEN_CHAIBU_METHOD = {
    "leap_bureau_forbidden": True,
    "bureau_change_forbidden": True,
    "transition_sequence": ["locate_solar_term_transition_day", "check_jiaji_fu_tou", "determine_yuan_and_bureau"],
    "zhengshou_condition": "transition_day_matches_jiaji_fu_tou",
    "chaibu_condition": "transition_day_does_not_match_fu_tou",
    "astronomical_hard_cutoff": True,
    "cutoff_boundary_rule": {"before_transition_moment": "old_bureau", "at_or_after_transition_moment": "new_bureau"},
    "critical_window_minutes": 15,
    "critical_window_action": "flag_warning_and_list_both_bureaus_reference_only",
}

YIN_YANG_DUN_BOUNDARY = {"yang_dun": "dongzhi_to_xiazhi", "yin_dun": "xiazhi_to_dongzhi"}
