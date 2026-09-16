from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Provenance:
    source_tier: int
    book: Optional[str] = None
    juan: Optional[str] = None
    pian: Optional[str] = None
    line_id: Optional[str] = None
    original_quote: Optional[str] = None
    mainstream_url: Optional[str] = None

    def is_undocumented(self) -> bool:
        return self.source_tier == 4
