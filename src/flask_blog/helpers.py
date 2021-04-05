from dateutil import parser as date_parser


def tags_from_form(form):
    if "tags" in form:
        tags = form["tags"].split(",")
    else:
        tags = []
    return tags


def parse_date_or_none(potential_date_str):
    try:
        return date_parser.parse(potential_date_str).date()
    except (TypeError, date_parser._parser.ParserError):
        return None


def convert_date_to_iso8601_string(date_obj):
    return date_obj.strftime("%Y-%m-%d")
