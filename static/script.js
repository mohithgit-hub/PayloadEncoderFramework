
document.addEventListener("DOMContentLoaded", function () {

    const navigationButtons = document.querySelectorAll(".nav-btn");
    const contentSections = document.querySelectorAll(".content-section");

    navigationButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const targetSection = button.dataset.section;

            navigationButtons.forEach(function (navButton) {
                navButton.classList.remove("active");
            });

            contentSections.forEach(function (section) {
                section.classList.remove("active");
            });

            button.classList.add("active");

            const selectedSection = document.getElementById(targetSection);

            if (selectedSection) {
                selectedSection.classList.add("active");
            }

        });

    });


    const encodingMethod = document.getElementById("encoding-method");
    const xorKeyGroup = document.getElementById("xor-key-group");
    const encodingPayload = document.getElementById("encoding-payload");
    const encodingOutput = document.getElementById("encoding-output");
    const xorKey = document.getElementById("xor-key");
    const encodeButton = document.getElementById("encode-btn");
    const decodeButton = document.getElementById("decode-btn");


    function updateXorKeyVisibility() {
        xorKeyGroup.hidden = encodingMethod.value !== "xor";
    }

    encodingMethod.addEventListener("change", updateXorKeyVisibility);
    updateXorKeyVisibility();


    async function processEncoding(operation) {

        const payload = encodingPayload.value;
        const method = encodingMethod.value;
        const key = xorKey.value;

        if (payload.trim() === "") {
            encodingOutput.value = "Please enter a text payload.";
            return;
        }

        if (method === "xor" && key.trim() === "") {
            encodingOutput.value = "Please enter an XOR key.";
            return;
        }

        if (!["base64", "xor", "rot13"].includes(method)) {
            encodingOutput.value = "Invalid encoding technique.";
            return;
        }

        encodingOutput.value = "Processing...";

        try {

            const response = await fetch("/api/encoding", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    payload: payload,
                    method: method,
                    operation: operation,
                    key: key
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Processing failed.");
            }

            encodingOutput.value = data.result;

        } catch (error) {
            encodingOutput.value = "Error: " + error.message;
        }

    }


    encodeButton.addEventListener("click", function () {
        processEncoding("encode");
    });

    decodeButton.addEventListener("click", function () {
        processEncoding("decode");
    });


    const obfuscationPayload = document.getElementById("obfuscation-payload");
    const obfuscationOutput = document.getElementById("obfuscation-output");
    const obfuscationMethod = document.getElementById("obfuscation-method");
    const obfuscateButton = document.getElementById("obfuscate-btn");
    const reverseButton = document.getElementById("reverse-btn");


    async function processObfuscation(operation) {

        const payload = obfuscationPayload.value;
        const method = obfuscationMethod.value;

        if (payload.trim() === "") {
            obfuscationOutput.value = "Please enter a text payload.";
            return;
        }

        if (!["random", "splitting", "reversible", "escape"].includes(method)) {
            obfuscationOutput.value = "Invalid obfuscation technique.";
            return;
        }

        obfuscationOutput.value = "Processing...";

        try {

            const response = await fetch("/api/obfuscation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    payload: payload,
                    method: method,
                    operation: operation
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Obfuscation failed.");
            }

            obfuscationOutput.value = data.result;

        } catch (error) {
            obfuscationOutput.value = "Error: " + error.message;
        }

    }


    obfuscateButton.addEventListener("click", function () {
        processObfuscation("obfuscate");
    });

    reverseButton.addEventListener("click", function () {
        processObfuscation("reverse");
    });


    const detectionPayload = document.getElementById("detection-payload");
    const detectButton = document.getElementById("detect-btn");
    const detectionStatus = document.getElementById("detection-status");
    const matchedSignature = document.getElementById("matched-signature");
    const detectionOutcome = document.getElementById("detection-outcome");


    async function processDetection() {

        const payload = detectionPayload.value;

        if (payload.trim() === "") {
            detectionStatus.textContent = "No input";
            matchedSignature.textContent = "None";
            detectionOutcome.textContent = "Please enter a text payload.";
            return;
        }

        detectionStatus.textContent = "Testing...";
        matchedSignature.textContent = "Checking...";
        detectionOutcome.textContent = "Comparing against simulated signatures.";

        detectButton.disabled = true;

        try {

            const response = await fetch("/api/detection", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    payload: payload
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Detection failed.");
            }

            detectionStatus.textContent = data.detected
                ? "DETECTED"
                : "NOT DETECTED";

            matchedSignature.textContent = data.matched_signature || "None";
            detectionOutcome.textContent = data.message;

        } catch (error) {

            detectionStatus.textContent = "ERROR";
            matchedSignature.textContent = "Unavailable";
            detectionOutcome.textContent = error.message;

        } finally {
            detectButton.disabled = false;
        }

    }


    detectButton.addEventListener("click", processDetection);


    const comparisonPanel = document.createElement("div");

    comparisonPanel.style.marginTop = "25px";
    comparisonPanel.style.padding = "20px";
    comparisonPanel.style.border = "1px solid #444";
    comparisonPanel.style.borderRadius = "10px";

    comparisonPanel.innerHTML = `
        <h3>Original vs Transformed Comparison</h3>
        <p>Select a transformation technique:</p>

        <select id="comparison-method">
            <option value="base64">Base64</option>
            <option value="rot13">ROT13</option>
            <option value="random">Random Character Insertion</option>
            <option value="splitting">Character Splitting</option>
            <option value="reversible">Reversible Transformation</option>
            <option value="escape">Escape-Sequence Obfuscation</option>
        </select>

        <br><br>

        <button type="button" id="compare-btn">
            Compare Payloads
        </button>

        <div id="comparison-results" style="margin-top: 20px;">
            <p>Comparison results will appear here.</p>
        </div>
    `;

    detectionPayload.insertAdjacentElement("afterend", comparisonPanel);

    const comparisonMethod = document.getElementById("comparison-method");
    const compareButton = document.getElementById("compare-btn");
    const comparisonResults = document.getElementById("comparison-results");


    async function comparePayloads() {

        const payload = detectionPayload.value;
        const method = comparisonMethod.value;

        if (payload.trim() === "") {
            comparisonResults.textContent = "Please enter a text payload first.";
            return;
        }

        compareButton.disabled = true;
        comparisonResults.textContent = "Comparing payloads...";

        try {

            const response = await fetch("/api/detection/compare", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    payload: payload,
                    method: method
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Comparison failed.");
            }

            comparisonResults.replaceChildren();

            const originalHeading = document.createElement("h4");
            originalHeading.textContent = "Original Payload Result";

            const originalStatus = document.createElement("p");
            originalStatus.textContent = "Status: " +
                (data.original.detected ? "DETECTED" : "NOT DETECTED");

            const originalSignature = document.createElement("p");
            originalSignature.textContent = "Matched Signature: " +
                (data.original.matched_signature || "None");

            const transformedHeading = document.createElement("h4");
            transformedHeading.textContent = "Transformed Payload";

            const transformedOutput = document.createElement("textarea");
            transformedOutput.readOnly = true;
            transformedOutput.rows = 3;
            transformedOutput.style.width = "100%";
            transformedOutput.value = data.transformed_payload;

            const transformedResultHeading = document.createElement("h4");
            transformedResultHeading.textContent = "Transformed Payload Result";

            const transformedStatus = document.createElement("p");
            transformedStatus.textContent = "Status: " +
                (data.transformed.detected ? "DETECTED" : "NOT DETECTED");

            const transformedSignature = document.createElement("p");
            transformedSignature.textContent = "Matched Signature: " +
                (data.transformed.matched_signature || "None");

            comparisonResults.append(
                originalHeading,
                originalStatus,
                originalSignature,
                document.createElement("hr"),
                transformedHeading,
                transformedOutput,
                transformedResultHeading,
                transformedStatus,
                transformedSignature
            );

        } catch (error) {

            comparisonResults.textContent = "Error: " + error.message;

        } finally {
            compareButton.disabled = false;
        }

    }


    compareButton.addEventListener("click", comparePayloads);


    const generateReportButton = document.getElementById("generate-report-btn");
    const totalTests = document.getElementById("total-tests");
    const totalDetected = document.getElementById("total-detected");
    const totalUndetected = document.getElementById("total-undetected");
    const reportTableBody = document.getElementById("report-table-body");
    const reportAnalysis = document.getElementById("report-analysis");


    async function generateReport() {

        generateReportButton.disabled = true;
        generateReportButton.textContent = "Generating...";

        try {

            const response = await fetch("/api/report");
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Report generation failed.");
            }

            const report = data.report;

            totalTests.textContent = report.total_tests;
            totalDetected.textContent = report.total_detected;
            totalUndetected.textContent = report.total_undetected;

            reportTableBody.replaceChildren();

            if (report.records.length === 0) {

                const row = document.createElement("tr");
                const cell = document.createElement("td");

                cell.colSpan = 6;
                cell.textContent = "No recorded outputs or comparison results.";

                row.appendChild(cell);
                reportTableBody.appendChild(row);

            } else {

                report.records.forEach(function (record) {

                    const row = document.createElement("tr");

                    const values = [
                        record.category,
                        record.technique,
                        record.original_payload,
                        record.transformed_payload,
                        record.original_detected === null
                            ? "Not tested"
                            : record.original_detected ? "Detected" : "Not detected",
                        record.transformed_detected === null
                            ? "Not tested"
                            : record.transformed_detected ? "Detected" : "Not detected"
                    ];

                    values.forEach(function (value) {

                        const cell = document.createElement("td");
                        cell.textContent = value;
                        row.appendChild(cell);

                    });

                    reportTableBody.appendChild(row);

                });

            }

            reportAnalysis.replaceChildren();

            const rate = document.createElement("p");
            rate.textContent = "Simulated Evasion Success Rate: " +
                report.evasion_success_rate + "%";

            reportAnalysis.appendChild(rate);

            report.insights.forEach(function (insight) {

                const paragraph = document.createElement("p");
                paragraph.textContent = insight;
                reportAnalysis.appendChild(paragraph);

            });

        } catch (error) {

            reportAnalysis.textContent = "Error: " + error.message;

        } finally {

            generateReportButton.disabled = false;
            generateReportButton.textContent = "Generate Report";

        }

    }


    generateReportButton.addEventListener("click", generateReport);


    const clearRecordsButton = document.createElement("button");
    clearRecordsButton.type = "button";
    clearRecordsButton.id = "clear-records-btn";
    clearRecordsButton.textContent = "Clear Records";
    clearRecordsButton.className = generateReportButton.className;
    clearRecordsButton.style.marginLeft = "10px";

    generateReportButton.insertAdjacentElement("afterend", clearRecordsButton);


    async function clearRecords() {

        const confirmed = window.confirm(
            "Are you sure you want to clear all recorded outputs and comparison results? This action cannot be undone."
        );

        if (!confirmed) {
            return;
        }

        clearRecordsButton.disabled = true;
        clearRecordsButton.textContent = "Clearing...";

        try {

            const response = await fetch("/api/report/clear", {
                method: "POST"
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Unable to clear report records.");
            }

            await generateReport();

            const message = document.createElement("p");
            message.textContent = data.message;
            reportAnalysis.prepend(message);

        } catch (error) {

            reportAnalysis.textContent = "Error: " + error.message;

        } finally {

            clearRecordsButton.disabled = false;
            clearRecordsButton.textContent = "Clear Records";

        }

    }


    clearRecordsButton.addEventListener("click", clearRecords);

});
