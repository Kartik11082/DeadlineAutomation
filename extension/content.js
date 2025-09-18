(() => {
    // Simple regex for dates in mm/dd/yyyy
    const dateRegex = /(\d{1,2}\/\d{1,2}\/\d{4})\s*:\s*(.+)/;

    let results = [];
    document.querySelectorAll("p").forEach(p => {
        const match = p.textContent.match(dateRegex);
        if (match) {
            results.push({
                date: match[1],
                event: match[2].trim()
            });
        }
    });

    chrome.runtime.sendMessage({
        type: "SEND_TO_SERVER",
        url: window.location.href,
        extracted: results
    }, (response) => {
        if (response.status === "ok") {
            console.log("Sent to server:", response.serverResponse);
        } else {
            console.error("Error sending:", response.error);
        }
    });

    // also return extracted results for popup
    return results;
})();
