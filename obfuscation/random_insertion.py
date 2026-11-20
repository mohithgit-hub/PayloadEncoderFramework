
import random
import string


def random_character_insertion(payload):

    characters = string.ascii_letters + string.digits + "!@#$%^&*"

    obfuscated_parts = []

    for char in payload:

        obfuscated_parts.append(char)

        random_char = random.choice(characters)

        obfuscated_parts.append(random_char)

    return "".join(obfuscated_parts)


def reverse_random_insertion(obfuscated_payload):

    return obfuscated_payload[::2]
