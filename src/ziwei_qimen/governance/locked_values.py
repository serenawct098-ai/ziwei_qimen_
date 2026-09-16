GENERAL_LOCKS = {
    "source_priority_order": ["user_ruling", "classical_text", "mainstream_consensus", "undocumented"],
    "school_closed_set": {
        "ziwei": ["nanpai_sanhe", "sihua_feixing"],
        "qimen": ["shijia_zhuanpan_chaibu"],
    },
    "modern_teaching_material_tier": "mainstream_consensus_subordinate",
    "confidence_annotation_required": True,
    "evidence_convergence_required": True,
    "numeric_verdict_forbidden": True,
    "invocation_mode_independence": True,
    "scene_independence": True,
    "interpretation_axis_parallel": True,
}

QIMEN_LOCKS = {
    "method": "shijia_zhuanpan_chaibu",
    "layout": "zhuanpan",
    "deity_system": ["zhifu", "tengshe", "taiyin", "liuhe", "baihu", "xuanwu", "jiudi", "jiutian"],
    "bureau_method": "chaibu",
    "yin_yang_dun_boundary": {"yang_dun": "dongzhi_to_xiazhi", "yin_dun": "xiazhi_to_dongzhi"},
    "solar_term_transition": "classical_sequence_with_astronomical_hard_cutoff",
    "sanqi_liuyi_direction": {
        "yang_dun": {"liuyi": "forward", "sanqi": "reverse"},
        "yin_dun": {"liuyi": "reverse", "sanqi": "forward"},
    },
    "center_palace_stem_host": "kun2_permanent",
    "tianqin_star": {
        "base_position": "center5",
        "static_host": "kun2",
        "dynamic_host": "tianrui_same_palace",
    },
    "kun2_dual_stem_ying": True,
    "eight_door_rotation": "fixed_clockwise_after_zhishi_anchor",
    "eight_deity_rotation": {"yang_dun": "clockwise", "yin_dun": "counterclockwise"},
    "nine_star_vitality": {"sheng_wo": "wang", "tong_wo": "xiang", "wo_ke": "xiu", "sheng_wo_reverse": "fei", "ke_wo": "qiu"},
    "eight_door_vitality": {"tong_wo": "wang", "sheng_wo": "xiang", "wo_sheng": "xiu", "wo_ke": "qiu", "ke_wo": "si"},
    "night_zi_hour": {
        "day_pillar": "stays_current_day",
        "hour_pillar": "advances_to_next_day_zi",
    },
    "scene_modes": ["yongshi", "yongren", "yongwu", "chuxing", "yongshen"],
    "interpretation_axes": ["fushi_daoxiang", "zhuke_boyi", "sancai_siti_xietong", "yongshen_liji"],
    "excluded_schools": ["yinpan", "feipan", "zhirun", "maoshan"],
}

ZIWEI_LOCKS = {
    "dual_core": {"body": "nanpai_sanhe", "use": "sihua_feixing"},
    "excluded_schools": ["beipai_qintian_sihua"],
    "late_zi_hour": {
        "range": "23:00:00-23:59:59",
        "effect": "next_day_single_chart",
        "zero_hour_range": "00:00:00-00:59:59_current_day",
    },
    "late_zi_hour_cross_use_forbidden_with": "qimen_night_zi_hour",
    "leap_month_effective_rule": {
        "day_1_to_15": "original_month",
        "day_16_to_end": "next_month",
    },
    "flow_month_across_solar_term": "keep_original_lunar_month_stem",
    "gengan_sihua": {
        "hua_lu": "taiyang",
        "hua_quan": "wuqu",
        "hua_ke": "tiantong",
        "hua_ji": "tianxiang",
    },
    "tiankui_tianyue_xin_year_exception": {"tiankui": "yin", "tianyue": "wu"},
    "ziwei_star_position_method": "lookup_table_only",
    "major_limit_start_palace": {
        "yang_male_yin_female": "one_before_life_palace_forward",
        "yin_male_yang_female": "one_after_life_palace_reverse",
    },
    "tianshang_tianshi_direction": {"tianshang": "six_before_life_palace", "tianshi": "six_after_life_palace"},
    "five_element_changsheng_direction": "gender_only_male_forward_female_reverse",
    "auxiliary_star_source": "classical_text_first_mainstream_fallback",
    "advanced_interpretation_methodology_tier": "mainstream_consensus",
    "scene_modes": ["yongren", "twins", "yongwu", "yongshen"],
    "decode_axes": ["tiyong", "palace_overlay", "sihua_causality", "star_pattern"],
    "numeric_verdict_forbidden": True,
}

SCENE_SPACE_LOCK = {
    "qimen": {
        "yongren": {"anchor": "birth_location", "moment": "birth_true_solar_time"},
        "yongshi": {"anchor": "questioner_realtime_location", "moment": "inquiry_true_solar_time"},
        "yongwu": {"anchor": "target_object_location", "moment": "survey_true_solar_time"},
        "chuxing": {"anchor": "departure_origin", "moment": "target_window_or_departure_true_solar_time"},
        "yongshen": {"anchor": "none", "moment": "intent_moment_true_solar_time"},
    },
    "ziwei": {
        "yongren": {"anchor": "birth_location", "moment": "birth_true_solar_time"},
        "twins": {"anchor": "birth_location_with_relativity_correction", "moment": "each_individual_birth_true_solar_time"},
        "yongwu": {"anchor": "residence_or_office_geometric_center", "moment": "natal_chart_as_body_survey_time_as_use"},
        "yongshen": {"anchor": "none", "moment": "intent_moment_true_solar_time"},
    },
}
