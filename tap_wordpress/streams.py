"""Stream type classes for tap-wordpress."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_wordpress.client import WordpressStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class ProductsStream(WordpressStream):
    """Define custom stream."""
    name = "products"
    path = "/wc/store/products"
    primary_keys = ["id"]
    replication_key = "id"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "products.json"
    # schema = th.PropertiesList(
    #     th.Property("name", th.StringType),
    #     th.Property("id", th.StringType),
    #     # th.Property("age", th.IntegerType),
    #     # th.Property("email", th.StringType),
    #     # th.Property("street", th.StringType),
    #     # th.Property("city", th.StringType),
    #     # th.Property("state", th.StringType),
    #     # th.Property("zip", th.StringType),
    # ).to_dict()


# class GroupsStream(WordpressStream):
#     """Define custom stream."""
#     name = "groups"
#     path = "/groups"
#     primary_keys = ["id"]
#     replication_key = "modified"
#     schema = th.PropertiesList(
#         th.Property("name", th.StringType),
#         th.Property("id", th.StringType),
#         th.Property("modified", th.DateTimeType),
#     ).to_dict()
