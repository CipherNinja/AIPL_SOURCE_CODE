document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector("form"); // Assuming the form tag is added to your HTML
    var usernameInput = document.getElementById("Username");
    var passwordInput = document.getElementById("Password");

    if (usernameInput && passwordInput) {
        form.addEventListener('submit', function(event) {
            // Username validation
            var username = usernameInput.value;
            if (username.length <= 7 || /[^a-zA-Z0-9]/.test(username)) {
                alert("Username must be at least 8 characters long and contain only alphanumeric characters.");
                event.preventDefault();
                return;
            }

            // Password validation
            var password = passwordInput.value;
            if (password.length < 8 || !/[A-Za-z]/.test(password) || !/[0-9]/.test(password)) {
                alert("Password must be at least 8 characters long and contain both letters and numbers.");
                event.preventDefault();
                return;
            }

            // Sanitize inputs to prevent XSS
            usernameInput.value = sanitizeInput(usernameInput.value);
            passwordInput.value = sanitizeInput(passwordInput.value);
        });
    } else {
        console.error("One or more input fields are missing from the form.");
    }
});

// Function to sanitize input to prevent XSS
function sanitizeInput(input) {
    const element = document.createElement('div');
    element.innerText = input;
    return element.innerHTML;
}
