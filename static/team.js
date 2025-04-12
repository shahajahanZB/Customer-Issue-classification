let currentTeamId = null;

async function fetchTeams() {
    try {
        const response = await fetch('/api/teams');
        const teams = await response.json();
        if (teams.error) {
            return;
        }
        renderTeams(teams);
    } catch (error) {
        // Handle error silently
    }
}

function renderTeams(teams) {
    const teamsList = document.getElementById('teams-list');
    if (!teamsList) {
        return;
    }
    
    teamsList.innerHTML = teams.map(team => `
        <div class="team-card" data-team-id="${team.id}" data-team-name="${team.name}" onclick="showTeamDetails(this, '${team.id}')">
            <h3>${team.name}</h3>
            <p>Category: ${team.category || team.name}</p>
            <p>${team.members.length} member(s)</p>
        </div>
    `).join('');
}

async function showTeamDetails(element, teamId) {
    // Update active state
    document.querySelectorAll('.team-card').forEach(card => card.classList.remove('active'));
    element.classList.add('active');
    
    currentTeamId = teamId;
    const teamName = element.dataset.teamName;
    
    // Update team name in header
    document.getElementById('selected-team-name').textContent = teamName;
    
    try {
        // Fetch and display team members
        const response = await fetch(`/api/teams/${teamId}`);
        const team = await response.json();
        if (team.error) {
            return;
        }
        renderTeamMembers(team.members);
    } catch (error) {
        // Handle error silently
    }
}

function renderTeamMembers(members) {
    const tbody = document.getElementById('team-members');
    if (!tbody) {
        return;
    }

    if (members.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="no-members">
                    <p>No team members yet.</p>
                    <p>Add team members to handle issues in this category.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = members.map(member => `
        <tr>
            <td>${member.name}</td>
            <td>${member.role}</td>
            <td>${member.email}</td>
            <td><span class="status ${member.status}">${member.status}</span></td>
            <td>${member.issues_solved}</td>
        </tr>
    `).join('');
}

async function handleAddMember(event) {
    event.preventDefault();
    
    if (!currentTeamId) {
        alert('Please select a team first');
        return;
    }

    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        role: formData.get('role')
    };
    
    try {
        const response = await fetch(`/api/teams/${currentTeamId}/members`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Failed to add member');
        }
        
        updateMembersList(result.member);
        event.target.reset();
    } catch (error) {
        alert('Failed to add member: ' + error.message);
    }
}

function updateMembersList(newMember) {
    const membersList = document.getElementById('team-members');
    if (!membersList) {
        return;
    }

    const currentMembers = membersList.innerHTML;
    
    const newMemberRow = `
        <tr>
            <td>${newMember.name}</td>
            <td>${newMember.role}</td>
            <td>${newMember.email}</td>
            <td><span class="status ${newMember.status}">${newMember.status}</span></td>
            <td>${newMember.issues_solved}</td>
        </tr>
    `;
    
    if (currentMembers.includes('No team members yet')) {
        membersList.innerHTML = newMemberRow;
    } else {
        membersList.innerHTML += newMemberRow;
    }
    
    // Update team card member count
    const teamCard = document.querySelector(`[data-team-id="${currentTeamId}"]`);
    if (!teamCard) {
        return;
    }

    const countDisplay = teamCard.querySelector('p:last-child');
    const currentCount = parseInt(countDisplay.textContent) || 0;
    countDisplay.textContent = `${currentCount + 1} member(s)`;
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    fetchTeams();
    
    // Show first team details on page load
    const firstTeam = document.querySelector('.team-card');
    if (firstTeam) {
        showTeamDetails(firstTeam, firstTeam.dataset.teamId);
    }

    // Simple form handling
    const addMemberForm = document.getElementById('addMemberForm');
    if (addMemberForm) {
        addMemberForm.addEventListener('submit', handleAddMember);
    }
});
