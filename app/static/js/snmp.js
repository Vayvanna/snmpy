document.getElementById('siteSelect').addEventListener('change', function() {
    const siteId = this.value;
    fetch(`/api/snmp_current?site_id=${siteId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('snmpData');
            container.innerHTML = data.map(item => `
                <div class="card mb-2">
                    <div class="card-body">
                        <h5>${item.site} - ${item.label}</h5>
                        <p>Value: ${item.value}<br>
                        Last Updated: ${item.timestamp}</p>
                    </div>
                </div>
            `).join('');
        });
});
