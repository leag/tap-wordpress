from typing import Optional
from urllib import parse


def get_next_page(links) -> Optional[int]:
    if not links:
        return None
    next_url = None
    for link in links.split(","):
        m = link.split(">", 1)
        url = m[0].strip()[1:]

        params = {}

        for param in m[1].split(";"):
            if not param:
                continue
            (k, v) = param.split("=")
            params[k.strip().lower()] = v.strip('"')
        if params.get("rel", None) == "next":
            next_url = url
            break
    if not next_url:
        return None
    params = dict(parse.parse_qsl(parse.urlsplit(next_url).query))
    return int(params["page"])
