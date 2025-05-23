// Make sure to include this script at the bottom of your HTML:
document.addEventListener('DOMContentLoaded', function () {
    fetchStats();
    fetchLogAnalytics();
});

// Fetch site stats (total, up, down) and update widgets
function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalSites').textContent = data.sites;
            document.getElementById('sitesUp').textContent = data.sites_up;
            document.getElementById('sitesDown').textContent = data.sites_down;
            renderPieChart(data.sites_up, data.sites_down);
        });
}

// Fetch log frequency data (e.g. counts per hour) and render chart
function fetchLogAnalytics() {
    fetch('/api/logs_summary')
        .then(res => res.json())
        .then(data => {
            renderLogFrequencyBarChart(data.hours, data.counts);
        });
}

// Pie Chart for Site Status
function renderPieChart(up, down) {
    const ctx = document.getElementById('statusPieChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Up', 'Down'],
            datasets: [{
                label: 'Site Status',
                data: [up, down],
                backgroundColor: ['#00e676', '#ef5350'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: 'Site Uptime Status' }
            }
        }
    });
}

// Bar Chart for Log Volume by Hour
function renderLogFrequencyBarChart(labels, data) {
    const ctx = document.getElementById('logBarChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Logs per Hour',
                data: data,
                backgroundColor: '#42a5f5'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Log Frequency by Hour' }
            }
        }
    });
}
