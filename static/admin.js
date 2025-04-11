// Fetch messages from the database and populate the table
async function fetchMessages() {
  try {
    const response = await fetch('/api/messages');
    const messages = await response.json();

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
    console.error('Error fetching messages:', error);
  }
}

// Add event listeners for classification filters
document.addEventListener('DOMContentLoaded', () => {
  fetchMessages(); // Fetch all messages by default
});