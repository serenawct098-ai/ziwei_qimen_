from __future__ import annotations

import re
from importlib.resources import files
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from ziwei_qimen.errors import DomainError, ErrorCode

_IANA_TIMEZONE = re.compile(r"^[A-Za-z_+\-]+(?:/[A-Za-z_+\-]+)+$")


def load_iana_timezone(name: str) -> ZoneInfo:
    if _IANA_TIMEZONE.fullmatch(name) is None:
        raise DomainError(ErrorCode.INVALID_TIMEZONE, f"unknown IANA timezone: {name}")
    try:
        resource = files("tzdata").joinpath("zoneinfo", *name.split("/"))
        with resource.open("rb") as handle:
            return ZoneInfo.from_file(handle, key=name)
    except (FileNotFoundError, IsADirectoryError, ZoneInfoNotFoundError) as error:
        raise DomainError(ErrorCode.INVALID_TIMEZONE, f"unknown IANA timezone: {name}") from error
