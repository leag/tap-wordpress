"""Stream type classes for tap-wordpress."""

from pathlib import Path

from tap_wordpress.client import WordpressStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ProductsStream(WordpressStream):
    """Define custom stream."""

    name = "products"
    path = "/wc/store/products"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "products.json"
