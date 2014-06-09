import re


fields = 'site', 'username', 'password', 'extra'
max_field_len = len(max(fields, key=len))


def find(search_term, pw_data):
    return [name for name in pw_data if re.search(search_term, name,
                                                  re.I)]
