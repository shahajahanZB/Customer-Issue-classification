// Load settings from localStorage
document.addEventListener('DOMContentLoaded', function() {
    // Theme settings
    const themeSelect = document.getElementById('themeSelect');
    themeSelect.value = localStorage.getItem('theme') || 'light';
    themeSelect.addEventListener('change', function() {
        localStorage.setItem('theme', this.value);
        applyTheme(this.value);
    });

    // Notification settings
    const emailNotif = document.getElementById('emailNotifications');
    emailNotif.checked = localStorage.getItem('emailNotifications') === 'true';
    emailNotif.addEventListener('change', function() {
        localStorage.setItem('emailNotifications', this.checked);
    });

    const desktopNotif = document.getElementById('desktopNotifications');
    desktopNotif.checked = localStorage.getItem('desktopNotifications') === 'true';
    desktopNotif.addEventListener('change', async function() {
        if (this.checked) {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                localStorage.setItem('desktopNotifications', true);
            } else {
                this.checked = false;
                alert('Desktop notifications permission denied');
            }
        } else {
            localStorage.setItem('desktopNotifications', false);
        }
    });

    // Refresh interval settings
    const refreshInterval = document.getElementById('refreshInterval');
    refreshInterval.value = localStorage.getItem('refreshInterval') || 30;
    refreshInterval.addEventListener('change', function() {
        localStorage.setItem('refreshInterval', this.value);
    });

    if (document.getElementById('resetRequestsTable')) {
        fetchResetRequests();
    }
});

function applyTheme(theme) {
    document.body.className = theme;
    // You can expand this function to apply more theme-specific styles
}

async function fetchResetRequests() {
    const response = await fetch('/api/reset-requests');
    const requests = await response.json();
    
    const tbody = document.getElementById('resetRequestsTable');
    tbody.innerHTML = requests.map(req => `
        <tr>
            <td>${req.member_name}</td>
            <td>${req.member_email}</td>
            <td>${req.requested_at}</td>
            <td>${req.status}</td>
            <td>
                ${req.status === 'pending' ? `
                    <button onclick="handleReset(${req.id}, '${req.member_email}')">Reset Password</button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

async function handleReset(requestId, email) {
    const newPassword = prompt('Enter new password for ' + email);
    if (!newPassword) return;

    try {
        const response = await fetch('/api/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                requestId,
                newPassword
            })
        });

        if (response.ok) {
            alert('Password has been reset');
            fetchResetRequests();
        } else {
            alert('Error resetting password');
        }
    } catch (error) {
        alert('Error resetting password');
    }
}
