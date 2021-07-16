"""REST client handling, including wordpressStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from tap_wordpress.helpers import get_next_page


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class WordpressStream(RESTStream):
    """Wordpress stream class."""

    url_base = "https://naipes.winterland.cl/wp-json"
    _LOG_REQUEST_METRIC_URLS = True

    # OR use a dynamic url_base:
    # @property
    # def url_base(self) -> str:
    #     """Return the API URL root, configurable via tap settings."""
    #     return self.config["api_url"]

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    # next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        links = response.headers.get("Link", None)
        if not links:
            return None
        return get_next_page(links)

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        params["per_page"] = self.config.get("per_page")
        if self.replication_key:
             params["order"] = "asc"
             params["orderby"] = self.replication_key
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
