document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector("form");
    var usernameInput = document.getElementById("Username");
    var passwordInput = document.getElementById("Password");

    if (usernameInput && passwordInput) {
        form.addEventListener('submit', function(event) {
            // Username validation using regex
            var username = usernameInput.value;

            // Regex to allow only alphanumeric characters and limit the length to 8-20 characters
            var usernameRegex = /^[a-zA-Z0-9]{8,20}$/;
            if (!usernameRegex.test(username)) {
                alert("Username must be between 8 to 20 characters long and contain only alphanumeric characters.");
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

// Function to validate email format
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// Function to sanitize input to prevent XSS
function sanitizeInput(input) {
    const element = document.createElement('div');
    element.innerText = input;
    return element.innerHTML;
}
