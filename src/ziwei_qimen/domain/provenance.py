"""來源、證據與計算 provenance 模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SourceKind = Literal[
    "classical_text",
    "mnemonic",
    "locked_adjudication",
    "official_calendar_data",
    "engineering_standard",
]

VerificationStatus = Literal[
    "verified",
    "adopted_by_user",
    "source_gap",
]


@dataclass(frozen=True, slots=True)
class SourceLocator:
    """來源內可回查的位置。"""

    volume: str | None = None
    section: str | None = None
    paragraph: str | None = None


@dataclass(frozen=True, slots=True)
class SourceRef:
    """唯一原文或裁定來源的識別資料。"""

    source_id: str
    source_title: str
    source_file: str
    locator: SourceLocator
    source_kind: SourceKind
    verification_status: VerificationStatus
    design_origin_note: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """某一排盤、推演或評級結論所使用的來源證據。"""

    source_ref: SourceRef
    rule_id: str
    original_quote: str | None = None
    application_note: str | None = None


@dataclass(frozen=True, slots=True)
class CalculationProvenance:
    """時間與天文計算的可重現資訊。"""

    timezone_data_version: str
    ephemeris_id: str
    ephemeris_version: str
    iers_data_version: str
    precision: Literal["second"]
