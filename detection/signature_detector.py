


SIMULATED_SIGNATURES = [
    "DEMO_SIGNATURE_ALPHA",
    "DEMO_SIGNATURE_BETA",
    "SUSPICIOUS_TEST_MARKER",
    "TEST_PATTERN_GAMMA",
    "SAMPLE_DETECTION_DELTA",
    "SECURITY_TEST_EPSILON",
    "DEMO_PATTERN_ZETA",
    "SIMULATED_THREAT_ETA",
    "CUSTOM_TEST_SIGNATURE_THETA",
    "OBFUSCATION_TEST_IOTA",
    "ENCODING_PATTERN_KAPPA",
    "DETECTION_MARKER_LAMBDA",
    "SIMULATED_PATTERN_MU",
    "TEST_SIGNATURE_NU",
    "SAMPLE_THREAT_XI",
    "SECURITY_MARKER_OMICRON",
    "DEMO_PAYLOAD_PI",
    "PATTERN_TEST_RHO",
    "SIMULATED_SIGNATURE_SIGMA",
    "CUSTOM_DETECTION_TAU"
]




def detect_signature(payload):

    if not isinstance(payload, str):
        raise ValueError("Payload must be a text string.")

    normalized_payload = payload.casefold()

    for signature in SIMULATED_SIGNATURES:

        if signature.casefold() in normalized_payload:

            return {
                "detected": True,
                "matched_signature": signature,
                "message": "Simulated signature detected."
            }

    return {
        "detected": False,
        "matched_signature": None,
        "message": "No simulated signature detected."
    }
