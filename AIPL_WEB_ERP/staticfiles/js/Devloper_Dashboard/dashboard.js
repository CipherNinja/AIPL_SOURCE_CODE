// Toggle Light/Dark Mode
document.getElementById('toggle-mode').addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    const modeText = document.body.classList.contains('light-mode') ? 'Dark Mode' : 'Light Mode';
    document.getElementById('toggle-mode').textContent = modeText;
});

// Simulated Data for Dynamic Content
function fetchLeaderboardData() {
    const data = [
        { name: 'Manish Kumar', progress: '50%', points: '1890 Points' },
        { name: 'Ravi Singh', progress: '69%', points: '2080 Points' },
        { name: 'Aakash Kumar', progress: '85%', points: '2840 Points' }
    ];

    const leaderboardList = document.getElementById('leaderboard-list');
    leaderboardList.innerHTML = '';
    data.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - ${item.progress} - ${item.points}`;
        leaderboardList.appendChild(li);
    });
}

fetchLeaderboardData();
