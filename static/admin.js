// Fetch query types from the database
async function fetchQueryTypes() {
    try {
        const response = await fetch('/api/query-types');
        const queryTypes = await response.json();
        return queryTypes;
    } catch (error) {
        console.error('Error fetching query types:', error);
        return [];
    }
}

// Fetch messages from the database and populate the table
async function fetchMessages() {
    try {
        const [messages, queryTypes] = await Promise.all([
            fetch('/api/messages').then(r => r.json()),
            fetchQueryTypes()
        ]);

        const tableBody = document.getElementById('message-table-body');
        tableBody.innerHTML = '';

        messages.forEach((message) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${message.queryNumber}</td>
                <td>${message.message}</td>
                <td>${message.routingTeam}</td>
                <td>${message.queryType}</td>
                <td>${message.confidentialityLevel}%</td>
                <td class="status ${message.status.toLowerCase()}">${message.status}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Add event listeners for classification filters
document.addEventListener('DOMContentLoaded', () => {
    fetchMessages(); // Fetch all messages by default
});