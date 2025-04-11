async function fetchAssignedQueries() {
    const response = await fetch('/api/member/queries');
    const queries = await response.json();
    
    const tableBody = document.getElementById('queries-table-body');
    tableBody.innerHTML = queries.map(query => `
        <tr>
            <td>${query.queryNumber}</td>
            <td>${query.message}</td>
            <td>${query.queryType}</td>
            <td class="status ${query.status.toLowerCase()}">${query.status}</td>
            <td>
                ${query.status !== 'Solved' ? 
                    `<button onclick="markAsSolved(${query.id})" class="solve-button">Mark as Solved</button>` : 
                    '<span class="solved">✓</span>'}
            </td>
        </tr>
    `).join('');
}

async function markAsSolved(queryId) {
    await fetch(`/api/member/queries/${queryId}/solve`, {
        method: 'POST'
    });
    fetchAssignedQueries();
}

document.addEventListener('DOMContentLoaded', fetchAssignedQueries);
