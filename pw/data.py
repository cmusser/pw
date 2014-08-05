import pw.util
import re


fields = 'site', 'username', 'password', 'extra'
max_field_len = len(max(fields, key=len))


def find(search_term, pw_data):
    return [name for name in pw_data if re.search(search_term, name,
                                                  re.I)]


def lookup_credential_for_edit(pw_data, search_term):
    names = find(search_term, pw_data)
    match_count = len(names)
    if match_count == 0:
        credential_name = search_term
    elif match_count == 1:
        credential_name = names[0]
    else:
        n = 0
        for name in names:
            n += 1
            print "\n{}.) {}".format(n, name)
        credential_name = names[pw.util.prompt_for_idx(names)]

    return credential_name
