
def xor_encode(payload, key):

    if not key:
        raise ValueError("XOR key cannot be empty.")

    payload_bytes = payload.encode("utf-8")
    key_bytes = key.encode("utf-8")

    result = bytearray()

    for index, byte in enumerate(payload_bytes):

        key_byte = key_bytes[index % len(key_bytes)]

        result.append(byte ^ key_byte)

    return result.hex()


def xor_decode(encoded_payload, key):

    if not key:
        raise ValueError("XOR key cannot be empty.")

    try:
        encrypted_bytes = bytes.fromhex(encoded_payload)
    except ValueError:
        raise ValueError("Invalid hexadecimal input.")

    key_bytes = key.encode("utf-8")

    result = bytearray()

    for index, byte in enumerate(encrypted_bytes):

        key_byte = key_bytes[index % len(key_bytes)]

        result.append(byte ^ key_byte)

    try:
        return result.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Incorrect XOR key or invalid encoded data.")
