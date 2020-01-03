import re


def camel2underscore(data: dict):
    result = {}
    for (k, v) in data.items():
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', k)
        k = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        result[k] = camel2underscore(v) if isinstance(v, dict) else v
    return result


def str_underscore2camel(s: str):
    s = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), s)
    return f'{s[0].upper()}{s[1:]}'
