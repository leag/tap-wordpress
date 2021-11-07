"""REST client handling, including wordpressStream base class."""

from pathlib import Path
from typing import Any, Dict, Optional

import requests
from linkheader_parser import parse
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class WordpressStream(RESTStream):
    """Wordpress stream class."""

    @property
    def url_base(self):
        if self.config.get("site"):
            return self.config.get("site", str()) + "/wp-json"

    _LOG_REQUEST_METRIC_URLS = True

    records_jsonpath = "$[*]"

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        link_header = response.headers.get("Link", None)
        return parse(link_header=link_header).get("next")

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token is not None:
            if next_page_token.get("page"):
                params["page"] = next_page_token.get("page")
            if next_page_token.get("per_page"):
                params["per_page"] = next_page_token.get("per_page")
            if next_page_token.get("order"):
                params["order"] = next_page_token.get("order")
            if next_page_token.get("orderby"):
                params["orderby"] = next_page_token.get("orderby")
        else:
            params["per_page"] = self.config.get("per_page")
            if self.replication_key:
                params["order"] = "asc"
                params["orderby"] = self.replication_key
        return params
