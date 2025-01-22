function login() {
    const username = prompt("Enter your username:");
    if (!username) {
        alert("You must enter a username!");
        return;
    }
    localStorage.setItem("username", username);
    alert(`Welcome, ${username}!`);
}
