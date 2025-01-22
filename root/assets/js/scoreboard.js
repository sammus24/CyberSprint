document.addEventListener('DOMContentLoaded', () => {
    const scoreboard = document.getElementById('scoreboard');
    const scores = JSON.parse(localStorage.getItem('scores')) || {};

    Object.entries(scores)
        .sort(([, scoreA], [, scoreB]) => scoreB - scoreA)
        .forEach(([username, score]) => {
            const entry = document.createElement('div');
            entry.textContent = `${username}: ${score} points`;
            scoreboard.appendChild(entry);
        });
});
