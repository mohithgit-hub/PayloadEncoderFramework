
SHIFT_VALUE = 3


def reversible_transform(payload):

    result = []

    for char in payload:
        result.append(chr(ord(char) + SHIFT_VALUE))

    return "".join(result)


def reverse_transform(transformed_payload):

    result = []

    for char in transformed_payload:
        result.append(chr(ord(char) - SHIFT_VALUE))

    return "".join(result)
