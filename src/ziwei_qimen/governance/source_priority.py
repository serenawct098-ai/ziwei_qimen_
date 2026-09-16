from enum import IntEnum


class SourceTier(IntEnum):
    USER_RULING = 1
    CLASSICAL_TEXT = 2
    MAINSTREAM_CONSENSUS = 3
    UNDOCUMENTED = 4


CLOSED_SCHOOL_SET = {
    "ziwei": ("nanpai_sanhe", "sihua_feixing"),
    "qimen": ("shijia_zhuanpan_chaibu",),
}

EXCLUDED_SCHOOLS = {
    "ziwei": ("beipai_qintian_sihua",),
    "qimen": ("yinpan", "feipan", "zhirun", "maoshan"),
}

CITATION_FORMAT = {
    SourceTier.USER_RULING: "\u3010\u4f7f\u7528\u8005\u88c1\u5b9a\u3011",
    SourceTier.CLASSICAL_TEXT: "\u300a\u66f8\u540d\u300b\u5377\u6b21\u30fb\u7bc7\u540d\uff1a\u300c\u539f\u6587\u9010\u5b57\u300d",
    SourceTier.MAINSTREAM_CONSENSUS: "\u3010\u4e3b\u6d41\u516c\u8a8d\u7248\u672c\u3011",
    SourceTier.UNDOCUMENTED: "\u539f\u6587\u672a\u8f09",
}


def resolve_conflict(user_ruling=None, classical_text=None, instruction=None, mainstream=None):
    if user_ruling is not None:
        return SourceTier.USER_RULING, user_ruling
    if classical_text is not None:
        return SourceTier.CLASSICAL_TEXT, classical_text
    if instruction is not None:
        return SourceTier.CLASSICAL_TEXT, instruction
    if mainstream is not None:
        return SourceTier.MAINSTREAM_CONSENSUS, mainstream
    return SourceTier.UNDOCUMENTED, None
