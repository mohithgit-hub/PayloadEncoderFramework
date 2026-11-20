
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from encoding.base64_encoder import encode_base64, decode_base64
from encoding.xor_encoder import xor_encode, xor_decode
from encoding.rot13_encoder import rot13_encode, rot13_decode

from obfuscation.random_insertion import (
    random_character_insertion,
    reverse_random_insertion
)

from obfuscation.string_splitting import (
    split_string,
    concatenate_string
)

from obfuscation.reversible_transform import (
    reversible_transform,
    reverse_transform
)

from obfuscation.escape_obfuscation import (
    escape_obfuscate,
    reverse_escape_obfuscation
)

from detection.signature_detector import detect_signature

from reporting.report_generator import (
    record_output,
    record_comparison,
    generate_report,
    clear_records
)

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": r"https://.*\.vercel\.app"
        }
    }
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/encoding", methods=["POST"])
def encoding():
    data = request.get_json(silent=True) or {}

    payload = data.get("payload")
    method = data.get("method")
    operation = data.get("operation")
    key = data.get("key", "")

    if not isinstance(payload, str):
        return jsonify({"error": "Please provide a valid text payload."}), 400

    try:
        if method == "base64":
            if operation == "encode":
                result = encode_base64(payload)
            elif operation == "decode":
                result = decode_base64(payload)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        elif method == "xor":
            if not isinstance(key, str) or not key:
                return jsonify({"error": "Please enter an XOR key."}), 400

            if operation == "encode":
                result = xor_encode(payload, key)
            elif operation == "decode":
                result = xor_decode(payload, key)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        elif method == "rot13":
            if operation == "encode":
                result = rot13_encode(payload)
            elif operation == "decode":
                result = rot13_decode(payload)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        else:
            return jsonify({"error": "Invalid encoding technique."}), 400

        if operation == "encode":
            record_output(payload, method.upper(), result, "Encoding")

        return jsonify({"success": True, "result": result})

    except (ValueError, UnicodeDecodeError):
        return jsonify({
            "error": "Invalid input or incorrect decoding key."
        }), 400


@app.route("/api/obfuscation", methods=["POST"])
def obfuscation():
    data = request.get_json(silent=True) or {}

    payload = data.get("payload")
    method = data.get("method")
    operation = data.get("operation")

    if not isinstance(payload, str):
        return jsonify({"error": "Please provide a valid text payload."}), 400

    try:
        if method == "random":
            if operation == "obfuscate":
                result = random_character_insertion(payload)
            elif operation == "reverse":
                result = reverse_random_insertion(payload)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        elif method == "splitting":
            if operation == "obfuscate":
                result = split_string(payload)
            elif operation == "reverse":
                result = concatenate_string(payload)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        elif method == "reversible":
            if operation == "obfuscate":
                result = reversible_transform(payload)
            elif operation == "reverse":
                result = reverse_transform(payload)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        elif method == "escape":
            if operation == "obfuscate":
                result = escape_obfuscate(payload)
            elif operation == "reverse":
                result = reverse_escape_obfuscation(payload)
            else:
                return jsonify({"error": "Invalid operation selected."}), 400

        else:
            return jsonify({
                "error": "Invalid obfuscation technique."
            }), 400

        if operation == "obfuscate":
            record_output(payload, method.upper(), result, "Obfuscation")

        return jsonify({"success": True, "result": result})

    except (ValueError, UnicodeError) as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/detection", methods=["POST"])
def detection():
    data = request.get_json(silent=True) or {}
    payload = data.get("payload")

    if not isinstance(payload, str):
        return jsonify({"error": "Please provide a valid text payload."}), 400

    result = detect_signature(payload)

    return jsonify({
        "success": True,
        "detected": result["detected"],
        "matched_signature": result["matched_signature"],
        "message": result["message"]
    })


@app.route("/api/detection/compare", methods=["POST"])
def compare_detection():
    data = request.get_json(silent=True) or {}

    payload = data.get("payload")
    method = data.get("method")

    if not isinstance(payload, str):
        return jsonify({"error": "Please provide a valid text payload."}), 400

    try:
        if method == "base64":
            transformed = encode_base64(payload)
        elif method == "rot13":
            transformed = rot13_encode(payload)
        elif method == "random":
            transformed = random_character_insertion(payload)
        elif method == "splitting":
            transformed = split_string(payload)
        elif method == "reversible":
            transformed = reversible_transform(payload)
        elif method == "escape":
            transformed = escape_obfuscate(payload)
        else:
            return jsonify({"error": "Invalid transformation selected."}), 400

        original_result = detect_signature(payload)
        transformed_result = detect_signature(transformed)

        record_comparison(
            payload,
            method.upper(),
            transformed,
            original_result["detected"],
            transformed_result["detected"]
        )

        return jsonify({
            "success": True,
            "transformed_payload": transformed,
            "original": {
                "detected": original_result["detected"],
                "matched_signature": original_result["matched_signature"]
            },
            "transformed": {
                "detected": transformed_result["detected"],
                "matched_signature": transformed_result["matched_signature"]
            }
        })

    except (ValueError, UnicodeError) as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/report", methods=["GET"])
def report():
    return jsonify({
        "success": True,
        "report": generate_report()
    })


@app.route("/api/report/clear", methods=["POST"])
def clear_report():
    clear_records()

    return jsonify({
        "success": True,
        "message": "All report records have been cleared.",
        "report": generate_report()
    })


if __name__ == "__main__":
    app.run(debug=True)
