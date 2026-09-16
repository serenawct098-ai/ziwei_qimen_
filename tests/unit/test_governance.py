from ziwei_qimen.governance.source_priority import SourceTier, resolve_conflict, CLOSED_SCHOOL_SET, EXCLUDED_SCHOOLS
from ziwei_qimen.governance.locked_values import GENERAL_LOCKS, QIMEN_LOCKS, ZIWEI_LOCKS, SCENE_SPACE_LOCK
from ziwei_qimen.governance.calendar_rules import ZIWEI_LATE_ZI_HOUR, QIMEN_NIGHT_ZI_HOUR, ZI_HOUR_RULE_CROSS_USE_FORBIDDEN
from ziwei_qimen.governance.gap_reporting import GapType, GAP_PRESENTATION_RULES
from ziwei_qimen.governance.output_rules import OUTPUT_FORMAT_LOCKS, REQUIRED_STEP_ELEMENTS
from ziwei_qimen.governance.delivery_checklist import DELIVERY_CHECKLIST
from ziwei_qimen.governance.glossary import GLOSSARY
from ziwei_qimen.governance.stage_mapping import STAGE_NAMES, STEP_STAGE_MAP, get_stage, get_stage_name, steps_in_stage
from ziwei_qimen.domain.provenance import Provenance


def test_source_priority_order():
    order = GENERAL_LOCKS["source_priority_order"]
    assert order == ["user_ruling", "classical_text", "mainstream_consensus", "undocumented"]


def test_resolve_conflict_prefers_user_ruling():
    tier, value = resolve_conflict(user_ruling="a", classical_text="b", mainstream="c")
    assert tier == SourceTier.USER_RULING
    assert value == "a"


def test_resolve_conflict_falls_back_to_classical():
    tier, value = resolve_conflict(classical_text="b", mainstream="c")
    assert tier == SourceTier.CLASSICAL_TEXT
    assert value == "b"


def test_closed_school_set_excludes_forbidden_schools():
    assert "beipai_qintian_sihua" not in CLOSED_SCHOOL_SET["ziwei"]
    assert "yinpan" not in CLOSED_SCHOOL_SET["qimen"]
    assert "beipai_qintian_sihua" in EXCLUDED_SCHOOLS["ziwei"]
    for school in ["yinpan", "feipan", "zhirun", "maoshan"]:
        assert school in EXCLUDED_SCHOOLS["qimen"]


def test_qimen_locks_deity_system_has_eight():
    assert len(QIMEN_LOCKS["deity_system"]) == 8


def test_qimen_locks_sanqi_liuyi_reverse_direction():
    yang = QIMEN_LOCKS["sanqi_liuyi_direction"]["yang_dun"]
    yin = QIMEN_LOCKS["sanqi_liuyi_direction"]["yin_dun"]
    assert yang["liuyi"] == "forward" and yang["sanqi"] == "reverse"
    assert yin["liuyi"] == "reverse" and yin["sanqi"] == "forward"


def test_ziwei_locks_gengan_sihua_full_set():
    sihua = ZIWEI_LOCKS["gengan_sihua"]
    assert sihua["hua_lu"] == "taiyang"
    assert sihua["hua_quan"] == "wuqu"
    assert sihua["hua_ke"] == "tiantong"
    assert sihua["hua_ji"] == "tianxiang"


def test_ziwei_locks_tiankui_tianyue_xin_year():
    exc = ZIWEI_LOCKS["tiankui_tianyue_xin_year_exception"]
    assert exc["tiankui"] == "yin"
    assert exc["tianyue"] == "wu"


def test_scene_space_lock_covers_all_modes():
    assert set(SCENE_SPACE_LOCK["qimen"].keys()) == {"yongren", "yongshi", "yongwu", "chuxing", "yongshen"}
    assert set(SCENE_SPACE_LOCK["ziwei"].keys()) == {"yongren", "twins", "yongwu", "yongshen"}


def test_zi_hour_rules_are_distinct_and_cross_use_forbidden():
    assert ZIWEI_LATE_ZI_HOUR["range_23_00_to_23_59_59"]["date_shift"] == "next_day"
    assert QIMEN_NIGHT_ZI_HOUR["range_23_00_to_23_59_59"]["day_pillar_shift"] == "none"
    assert ZI_HOUR_RULE_CROSS_USE_FORBIDDEN is True


def test_gap_types_cover_four_categories():
    assert len(GapType) == 4
    for gap_type in GapType:
        assert gap_type in GAP_PRESENTATION_RULES


def test_output_rules_forbid_conversational_text():
    assert "no_conversational_preamble_or_closing_text_in_formal_spec_documents" in OUTPUT_FORMAT_LOCKS


def test_required_step_elements_has_seven():
    assert len(REQUIRED_STEP_ELEMENTS) == 7


def test_delivery_checklist_has_27_items():
    assert len(DELIVERY_CHECKLIST) == 27
    ids = [item["id"] for item in DELIVERY_CHECKLIST]
    assert ids == list(range(1, 28))


def test_glossary_contains_key_terms():
    for term in ["true_solar_time", "late_zi_hour_ziwei", "night_zi_hour_qimen", "forward_dependency", "dual_track"]:
        assert term in GLOSSARY


def test_provenance_undocumented_flag():
    p = Provenance(source_tier=4)
    assert p.is_undocumented() is True
    p2 = Provenance(source_tier=2, book="\u300a\u7d2b\u5fae\u6578\u5168\u66f8\u300b", juan="\u5377\u4e8c")
    assert p2.is_undocumented() is False


def test_stage_mapping_has_118_steps():
    assert len(STEP_STAGE_MAP) == 118


def test_stage_mapping_no_duplicate_and_five_stages():
    assert len(set(STEP_STAGE_MAP.values())) == 5
    assert set(STAGE_NAMES.keys()) == {1, 2, 3, 4, 5}


def test_stage_one_covers_intent_and_setup():
    for step in ["IN01", "IN02", "IN03", "Z00", "Z01", "Z02", "Z03", "Z04", "Q00", "Q01", "Q02", "Q03", "Q04"]:
        assert get_stage(step) == 1


def test_stage_three_is_yongshen_only():
    ziwei_yongshen_steps = ["PZ01", "PZ02", "PZ03", "PZ04", "PZ05", "PZ06", "PZ07"]
    qimen_yongshen_steps = ["PQ01", "PQ02", "PQ03", "PQ04", "PQ05"]
    for step in ziwei_yongshen_steps + qimen_yongshen_steps:
        assert get_stage(step) == 3
    assert set(steps_in_stage(3)) == set(ziwei_yongshen_steps + qimen_yongshen_steps)


def test_stage_two_excludes_yongshen_steps():
    assert get_stage("Z32") == 2
    assert get_stage("L07") == 2
    assert get_stage("Q16") == 2
    assert "PZ01" not in steps_in_stage(2)
    assert "PQ01" not in steps_in_stage(2)


def test_stage_four_covers_causality_steps():
    assert get_stage("L08") == 4
    assert get_stage("PZ08") == 4
    assert get_stage("PZ24") == 4
    assert get_stage("PQ06") == 4
    assert get_stage("PQ18") == 4


def test_stage_five_covers_output_steps():
    for step in ["PZ25", "PZ26", "PZ27", "PZ28", "PQ19", "PQ20", "PQ21"]:
        assert get_stage(step) == 5


def test_get_stage_name_matches_stage_names_table():
    assert get_stage_name("PZ01") == STAGE_NAMES[3]
    assert get_stage_name("Z00") == STAGE_NAMES[1]
    assert get_stage_name("PQ21") == STAGE_NAMES[5]
