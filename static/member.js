async function fetchTeamQueries() {
    const response = await fetch('/api/member/team-queries');
    const queries = await response.json();
    renderQueries('team-queries', queries);
}

function renderQueries(containerId, queries) {
    const container = document.getElementById(containerId);
    container.innerHTML = queries.map(query => `
        <div class="query-card">
            <h3>#${query.queryNumber}</h3>
            <p>${query.message}</p>
            <div class="query-footer">
                <span class="query-type">${query.queryType}</span>
                <span class="status ${query.status.toLowerCase()}">${query.status}</span>
                <button onclick="pickTask(${query.id})">Pick Up</button>
            </div>
        </div>
    `).join('') || '<p class="no-items">No queries available</p>';
}

async function pickTask(queryId) {
    const response = await fetch(`/api/member/pick-task/${queryId}`, {
        method: 'POST'
    });
    if (response.ok) {
        fetchTeamQueries();
    }
}

async function markAsSolved(queryId) {
    try {
        const response = await fetch(`/api/member/queries/${queryId}/solve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to mark task as solved');
        }

        // Redirect to resolved tasks page after successful update
        window.location.href = '/member/resolved-tasks';
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to mark task as solved');
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', fetchTeamQueries);
