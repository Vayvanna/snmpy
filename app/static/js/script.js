// script.js

// Example: alert when page loads
window.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded");
    // alert("Welcome to SNMPy!");
});


async function updateSiteStatuses() {
    try {
        const response = await fetch("/api/sites_status");
        const data = await response.json();

        for (const id in data) {
            const status = data[id];
            const marker = document.getElementById(`marker-${id}`);
            if (marker) {
                if (status === "up") {
                    marker.setAttribute("fill", "green");
                } else {
                    marker.setAttribute("fill", "red");
                }
            }
        }
    } catch (error) {
        console.error("Failed to fetch site status:", error);
    }
}

// Call every 15 seconds
setInterval(updateSiteStatuses, 15000);
