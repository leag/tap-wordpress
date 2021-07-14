"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests

from tap_wordpress.tap import TapWordpress
from tap_wordpress.helpers import get_next_page

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    # TODO: Initialize minimal tap config
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapWordpress, config=SAMPLE_CONFIG)
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.


def test_link():
    link = '<https://naipes.winterland.cl/wp-json/wc/store/products?page=1>; rel="prev", <https://naipes.winterland.cl/wp-json/wc/store/products?page=3>; rel="next"'
    next_link = get_next_page(link)
    assert next_link == 3
    link = '<https://naipes.winterland.cl/wp-json/wc/store/products?page=141&per_page=100>; rel="prev"'
    next_link = get_next_page(link)
    assert next_link == None