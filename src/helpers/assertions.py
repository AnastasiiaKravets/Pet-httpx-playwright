from collections.abc import Iterable
from typing import Any


def assert_unique_field(items: Iterable[Any], field: str) -> None:
    seen = set()
    duplicates = set()

    for item in items:
        value = getattr(item, field)

        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    assert not duplicates, f"Duplicate values found in '{field}': {duplicates}"
