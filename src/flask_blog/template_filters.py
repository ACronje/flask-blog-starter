from urllib.parse import urlencode


def querystring_active(existing_query_string_dict, key, value):
    querystring_set = {(key, value)}
    if not existing_query_string_dict or not querystring_set:
        return False
    existing_query_string_set = set(existing_query_string_dict.items())
    return (
        existing_query_string_set.intersection(querystring_set)
        == querystring_set
    )


def querystring_toggler(existing_query_string_dict, key, value):
    qs = {key: value}
    querystring = existing_query_string_dict.copy()
    if querystring_active(existing_query_string_dict, key, value):
        querystring.pop(key)
    else:
        querystring.update(qs)
    return urlencode(querystring)
