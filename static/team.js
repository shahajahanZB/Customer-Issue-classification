let currentTeamId = null;

async function fetchTeams() {
    try {
        const response = await fetch('/api/teams');
        const teams = await response.json();
        if (teams.error) {
            console.error('Error fetching teams:', teams.error);
            return;
        }
        renderTeams(teams);
    } catch (error) {
        console.error('Failed to fetch teams:', error);
    }
}

function renderTeams(teams) {
    const teamsList = document.getElementById('teams-list');
    if (!teamsList) {
        console.error('teams-list element not found');
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
            console.error('Error fetching team details:', team.error);
            return;
        }
        renderTeamMembers(team.members);
    } catch (error) {
        console.error('Failed to fetch team details:', error);
    }
}

function renderTeamMembers(members) {
    const tbody = document.getElementById('team-members');
    if (!tbody) {
        console.error('team-members element not found');
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
        addMemberPopup.classList.remove('active');
    } catch (error) {
        alert('Failed to add member: ' + error.message);
    }
}

function updateMembersList(newMember) {
    const membersList = document.getElementById('team-members');
    if (!membersList) {
        console.error('team-members element not found');
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
        console.error('Team card element not found');
        return;
    }

    const countDisplay = teamCard.querySelector('p:last-child');
    const currentCount = parseInt(countDisplay.textContent) || 0;
    countDisplay.textContent = `${currentCount + 1} member(s)`;
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing...');
    fetchTeams();
});

// Show first team details on page load
document.addEventListener('DOMContentLoaded', () => {
    const firstTeam = document.querySelector('.team-card');
    if (firstTeam) {
        showTeamDetails(firstTeam, firstTeam.dataset.teamId);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const openAddMemberBtn = document.getElementById('openAddMemberBtn');
    const addMemberPopup = document.getElementById('addMemberPopup');
    const closePopupBtn = document.querySelector('.close-popup');
    const addMemberForm = document.getElementById('addMemberForm');

    // Open popup
    openAddMemberBtn.addEventListener('click', () => {
        addMemberPopup.classList.add('active');
    });

    // Close popup when clicking X button
    closePopupBtn.addEventListener('click', () => {
        addMemberPopup.classList.remove('active');
    });

    // Close popup when clicking outside
    addMemberPopup.addEventListener('click', (e) => {
        if (e.target === addMemberPopup) {
            addMemberPopup.classList.remove('active');
        }
    });

    // Handle form submission
    addMemberForm.addEventListener('submit', function(event) {
        event.preventDefault();
        handleAddMember(event);
        addMemberPopup.classList.remove('active');
    });
});
