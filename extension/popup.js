document.getElementById("extractBtn").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content.js"]
    }, (results) => {
        const list = document.getElementById("resultList");
        list.innerHTML = "";

        // results[0].result contains the return value from content.js
        if (results && results[0].result && results[0].result.length > 0) {
            results[0].result.forEach(item => {
                const li = document.createElement("li");
                li.textContent = `${item.date} → ${item.event}`;
                list.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "No deadlines found.";
            list.appendChild(li);
        }
    });
});
