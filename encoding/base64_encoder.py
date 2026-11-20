
import base64


def encode_base64(payload):
    encoded_bytes = base64.b64encode(payload.encode("utf-8"))
    return encoded_bytes.decode("utf-8")


def decode_base64(encoded_payload):
    decoded_bytes = base64.b64decode(
        encoded_payload,
        validate=True
    )
    return decoded_bytes.decode("utf-8")
