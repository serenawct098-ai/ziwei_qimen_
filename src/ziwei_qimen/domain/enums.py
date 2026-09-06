"""系統固定列舉。"""

from __future__ import annotations

from enum import IntEnum, StrEnum


class Stem(StrEnum):
    """十天干。"""

    JIA = "甲"
    YI = "乙"
    BING = "丙"
    DING = "丁"
    WU = "戊"
    JI = "己"
    GENG = "庚"
    XIN = "辛"
    REN = "壬"
    GUI = "癸"


class Branch(StrEnum):
    """十二地支。"""

    ZI = "子"
    CHOU = "丑"
    YIN = "寅"
    MAO = "卯"
    CHEN = "辰"
    SI = "巳"
    WU = "午"
    WEI = "未"
    SHEN = "申"
    YOU = "酉"
    XU = "戌"
    HAI = "亥"


class Gender(StrEnum):
    """出生性別。"""

    FEMALE = "female"
    MALE = "male"


class Grade(StrEnum):
    """紫微與奇門共用的非數值五級輸出。"""

    GREAT_AUSPICIOUS = "大吉"
    MINOR_AUSPICIOUS = "小吉"
    NEUTRAL = "平"
    MINOR_INAUSPICIOUS = "小凶"
    GREAT_INAUSPICIOUS = "大凶"


class DecisionBand(StrEnum):
    """25 格整合層的行動帶。"""

    EXPLOIT_NOW = "exploit_now"
    PREPARE_EXECUTE = "prepare_execute"
    MONITOR = "monitor"
    CONSERVE = "conserve"
    RETREAT = "retreat"


class QuestionCategory(StrEnum):
    """奇門與雙軌已支援問題類型。"""

    CAREER = "career"
    WEALTH = "wealth"
    RELATIONSHIP = "relationship"
    HEALTH = "health"
    TRAVEL = "travel"
    EVENT_DEVELOPMENT = "event_development"


class PalaceName(StrEnum):
    """紫微十二宮。"""

    LIFE = "命宮"
    SIBLINGS = "兄弟宮"
    SPOUSE = "夫妻宮"
    CHILDREN = "子女宮"
    WEALTH = "財帛宮"
    HEALTH = "疾厄宮"
    TRAVEL = "遷移宮"
    FRIENDS = "交友宮"
    CAREER = "官祿宮"
    PROPERTY = "田宅宮"
    MENTAL = "福德宮"
    PARENTS = "父母宮"


class PalaceNumber(IntEnum):
    """奇門九宮數。"""

    KAN_1 = 1
    KUN_2 = 2
    ZHEN_3 = 3
    XUN_4 = 4
    CENTER_5 = 5
    QIAN_6 = 6
    DUI_7 = 7
    GEN_8 = 8
    LI_9 = 9


class Door(StrEnum):
    """奇門八門。"""

    REST = "休"
    LIFE = "生"
    HURT = "傷"
    OBSTRUCT = "杜"
    SCENERY = "景"
    DEATH = "死"
    FEAR = "驚"
    OPEN = "開"


class Deity(StrEnum):
    """轉盤奇門八神。"""

    CHIEF = "值符"
    TENG_SHE = "螣蛇"
    TAI_YIN = "太陰"
    LIU_HE = "六合"
    BAI_HU = "白虎"
    XUAN_WU = "玄武"
    JIU_DI = "九地"
    JIU_TIAN = "九天"


class Star(StrEnum):
    """奇門九星。"""

    TIAN_PENG = "天蓬"
    TIAN_RUI = "天芮"
    TIAN_CHONG = "天沖"
    TIAN_FU = "天輔"
    TIAN_QIN = "天禽"
    TIAN_XIN = "天心"
    TIAN_ZHU = "天柱"
    TIAN_REN = "天任"
    TIAN_YING = "天英"
