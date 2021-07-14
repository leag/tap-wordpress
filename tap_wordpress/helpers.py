from typing import Optional
from urllib import parse


def get_next_page(links) -> Optional[int]:
    if not links:
        return None
    url = None
    for l in links.split(","):
        m = l.split(">", 1)
        url = m[0].strip()[1:]

        params = {}

        for p in m[1].split(";"):
            if not p:
                continue

            (k, v) = p.split("=")
            params[k.strip().lower()] = v.strip()

        if params.get("rel", None) != "next":
            continue
    if not url:
        return None
    params = dict(parse.parse_qsl(parse.urlsplit(url).query))
    return int(params["page"])
