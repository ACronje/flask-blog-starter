def tags_from_form(form):
    if "tags" in form:
        tags = form["tags"].split(",")
    else:
        tags = []
    return tags
