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
});

function applyTheme(theme) {
    document.body.className = theme;
    // You can expand this function to apply more theme-specific styles
}
