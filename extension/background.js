chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            // run directly instead of separate content.js
            return document.documentElement.outerHTML;
        }
    }, (injectionResults) => {
        if (injectionResults && injectionResults[0]) {
            const htmlContent = injectionResults[0].result;

            fetch("http://127.0.0.1:5000/receive-html", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url: tab.url,
                    html: htmlContent
                })
            })
                .then(res => res.json())
                .then(data => console.log("Server response:", data))
                .catch(err => console.error("Error sending HTML:", err));
        }
    });
});
