
REPORT_DATA = []


def record_output(payload, technique, output, category):
    REPORT_DATA.append({
        "type": "output",
        "category": category,
        "technique": technique,
        "original_payload": payload,
        "transformed_payload": output,
        "original_detected": None,
        "transformed_detected": None
    })


def record_comparison(
    payload,
    technique,
    transformed_payload,
    original_detected,
    transformed_detected
):
    REPORT_DATA.append({
        "type": "comparison",
        "category": "Evasion Testing",
        "technique": technique,
        "original_payload": payload,
        "transformed_payload": transformed_payload,
        "original_detected": original_detected,
        "transformed_detected": transformed_detected
    })


def clear_records():
    REPORT_DATA.clear()


def generate_report():
    comparisons = [
        record for record in REPORT_DATA
        if record["type"] == "comparison"
    ]

    total_tests = len(comparisons)

    total_detected = sum(
        1 for record in comparisons
        if record["transformed_detected"] is True
    )

    total_undetected = sum(
        1 for record in comparisons
        if record["transformed_detected"] is False
    )

    eligible_tests = [
        record for record in comparisons
        if record["original_detected"] is True
    ]

    successful_evasions = sum(
        1 for record in eligible_tests
        if record["transformed_detected"] is False
    )

    eligible_count = len(eligible_tests)

    evasion_success_rate = (
        round((successful_evasions / eligible_count) * 100, 2)
        if eligible_count > 0 else 0
    )

    insights = []

    if total_tests == 0:
        insights.append("No comparison tests have been performed yet.")
    else:
        insights.append(
            f"A total of {total_tests} comparison tests were performed."
        )
        insights.append(
            f"{total_detected} transformed payloads were detected."
        )
        insights.append(
            f"{total_undetected} transformed payloads were not detected."
        )

        if eligible_count > 0:
            insights.append(
                f"The simulated evasion success rate was "
                f"{evasion_success_rate}% across {eligible_count} eligible comparisons."
            )
        else:
            insights.append(
                "No original payloads were detected, so an evasion success rate could not be calculated."
            )

        insights.append(
            "These results represent the simulated signature detector, not real antivirus performance."
        )

    return {
        "records": REPORT_DATA,
        "total_tests": total_tests,
        "total_detected": total_detected,
        "total_undetected": total_undetected,
        "successful_evasions": successful_evasions,
        "evasion_success_rate": evasion_success_rate,
        "insights": insights
    }
