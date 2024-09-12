// Show notification panel
document.querySelector('.notification-button').addEventListener('click', () => {
const notificationPanel = document.getElementById('notificationPanel');
notificationPanel.style.display = notificationPanel.style.display === 'none' ? 'block' : 'none';
});
