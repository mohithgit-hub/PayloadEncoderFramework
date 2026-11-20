
def split_string(payload, chunk_size=3):

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    parts = [
        payload[index:index + chunk_size]
        for index in range(0, len(payload), chunk_size)
    ]

    return " + ".join(parts)


def concatenate_string(split_payload):

    parts = split_payload.split(" + ")

    return "".join(parts)
