import re


def sanitize_filename(filename):
    sanitized = re.sub(r'[\/<>|:&;`?*\^%$#@!=+[\]{}(),\"\s]', '_', filename)
    sanitized = re.sub(r'^\.*|\.*$', '', sanitized)
    sanitized = sanitized[:255]
    return sanitized