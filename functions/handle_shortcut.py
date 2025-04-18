import mitmproxy

def shortcut_function(flow: mitmproxy.http.HTTPFlow, shortcut_map=None):
    q = flow.request.query.get("q", None)

    if not shortcut_map or not q:
        return False  # No shortcut map or no query => nothing to do

    for keyword, redirect_url in shortcut_map.items():
        # Case 1: If the query is in the format "keyword:actual_search"
        if ":" in q:
            key_part, value_part = q.split(":", 1)
            key_part = key_part.strip()
            value_part = value_part.strip()

            if key_part == keyword and value_part:
                flow.response = mitmproxy.http.Response.make(
                    302,
                    b"",
                    {"Location": redirect_url + value_part}
                )
                return True  # ✅ Only here, a redirect happened → count it

        # Case 2: If query is exactly the keyword (no colon), and we want direct redirect
        if q.strip() == keyword:
            flow.response = mitmproxy.http.Response.make(
                302,
                b"",
                {"Location": redirect_url}
            )
            return True  # ✅ Also here, a redirect happened → count it

    return False  # ❌ No valid redirect happened → don’t count it
