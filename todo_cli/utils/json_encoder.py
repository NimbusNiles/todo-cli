"""Enhanced json encoder to deal with dataclasses."""

from json import JSONEncoder
import dataclasses
from typing import Any


class EnhancedJSONEncoder(JSONEncoder):
    """Enhance JSON encoder for simple dataclasses."""

    def default(self, obj) -> dict[str, Any] | Any:
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        else:
            return super().default(obj)
