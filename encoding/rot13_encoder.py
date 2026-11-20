
def rot13_encode(payload):

    result = []

    for char in payload:

        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))

        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))

        else:
            result.append(char)

    return ''.join(result)


def rot13_decode(payload):

    return rot13_encode(payload)
