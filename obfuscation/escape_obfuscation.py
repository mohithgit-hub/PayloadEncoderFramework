
def escape_obfuscate(payload):

    result = []

    for char in payload:
        result.append("\\u{:04x}".format(ord(char)))

    return "".join(result)


def reverse_escape_obfuscation(obfuscated_payload):

    if len(obfuscated_payload) % 6 != 0:
        raise ValueError("Invalid escape-sequence input.")

    result = []

    for index in range(0, len(obfuscated_payload), 6):

        sequence = obfuscated_payload[index:index + 6]

        if not sequence.startswith("\\u"):
            raise ValueError("Invalid Unicode escape sequence.")

        try:
            character_code = int(sequence[2:], 16)
            result.append(chr(character_code))

        except ValueError:
            raise ValueError("Invalid Unicode escape sequence.")

        if character_code > 0x10FFFF or 0xD800 <= character_code <= 0xDFFF:
            raise ValueError("Invalid Unicode character.")

    return "".join(result)
