def get_unique_name(name, elems):
    """
    Return a unique version of the name indicated by incrementing a numeral
    at the end. Stop when the name no longer appears in the indicated list of
    elements.

    """
    digits = []
    for c in reversed(name):
        if c.isdigit():
            digits.append(c)
        else:
            break

    stem = name[0:len(name) - len(digits)]
    val = ''.join(digits)[::-1] or 0
    i = int(val)

    while True:
        i += 1
        new_name = ''.join([stem, str(i)])
        if new_name not in elems:
            break

    return new_name


def get_lower_camel_case(name):
    return name[0].lower() + name[1:] if name else name