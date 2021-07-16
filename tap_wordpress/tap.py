"""wordpress tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_wordpress.streams import (
    ProductsStream,
)

STREAM_TYPES = [
    ProductsStream,
]


class TapWordpress(Tap):
    """Wordpress tap class."""
    name = "tap-wordpress"

    config_jsonschema = th.PropertiesList(
        th.Property("per_page", th.IntegerType, default=100)
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
