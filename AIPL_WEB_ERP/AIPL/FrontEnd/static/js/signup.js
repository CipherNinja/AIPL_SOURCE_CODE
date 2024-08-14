document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById("signupForm");
    var nameInput = document.getElementById("name");
    var emailInput = document.getElementById("email");
    var passwordInput = document.getElementById("password");
    var confirmPasswordInput = document.getElementById("confirmPassword");

    if (nameInput && emailInput && passwordInput && confirmPasswordInput) {
        form.addEventListener('submit', function(event) {
            // Name validation using regex
            var name = nameInput.value;
            var nameRegex = /^[a-zA-Z0-9]{8,}$/;
            if (!nameRegex.test(name)) {
                alert("Name must be greater than 7 characters and contain only alphanumeric characters.");
                event.preventDefault();
                return;
            }

            // Email validation using regex
            var email = emailInput.value;
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert("Please enter a valid email address.");
                event.preventDefault();
                return;
            }

            // Password validation
            var password = passwordInput.value;
            if (password.length < 8 || !/[A-Za-z]/.test(password) || !/[0-9]/.test(password)) {
                alert("Password must be greater than 8 characters and contain both letters and numbers.");
                event.preventDefault();
                return;
            }

            // Confirm Password validation
            var confirmPassword = confirmPasswordInput.value;
            if (password !== confirmPassword) {
                alert("Passwords do not match.");
                event.preventDefault();
                return;
            }

            // Basic sanitization for XSS and SQL injection prevention
            var sanitizeInput = function(input) {
                return input.replace(/[<>&'"]/g, function(c) {
                    return {'<':'&lt;', '>':'&gt;', '&':'&amp;', "'":'&#39;', '"':'&quot;'}[c];
                });
            };

            nameInput.value = sanitizeInput(nameInput.value);
            emailInput.value = sanitizeInput(emailInput.value);
            passwordInput.value = sanitizeInput(passwordInput.value);
            confirmPasswordInput.value = sanitizeInput(confirmPasswordInput.value);
        });

        // Password criteria message
        var passwordMessageItems = document.getElementsByClassName("password-message-item");
        var passwordMessage = document.getElementById("password-message");

        if (passwordInput && passwordMessage && passwordMessageItems.length >= 4) {
            passwordInput.onfocus = function () { 
                passwordMessage.style.display = "block"; 
            } 

            passwordInput.onblur = function () { 
                passwordMessage.style.display = "none"; 
            } 

            passwordInput.onkeyup = function () { 
                // Checking uppercase letters 
                let uppercaseRegex = /[A-Z]/g; 
                if (passwordInput.value.match(uppercaseRegex)) { 
                    passwordMessageItems[1].classList.remove("invalid"); 
                    passwordMessageItems[1].classList.add("valid"); 
                } else { 
                    passwordMessageItems[1].classList.remove("valid"); 
                    passwordMessageItems[1].classList.add("invalid"); 
                } 

                // Checking lowercase letters 
                let lowercaseRegex = /[a-z]/g; 
                if (passwordInput.value.match(lowercaseRegex)) { 
                    passwordMessageItems[0].classList.remove("invalid"); 
                    passwordMessageItems[0].classList.add("valid"); 
                } else { 
                    passwordMessageItems[0].classList.remove("valid"); 
                    passwordMessageItems[0].classList.add("invalid"); 
                } 

                // Checking the number 
                let numbersRegex = /[0-9]/g; 
                if (passwordInput.value.match(numbersRegex)) { 
                    passwordMessageItems[2].classList.remove("invalid"); 
                    passwordMessageItems[2].classList.add("valid"); 
                } else { 
                    passwordMessageItems[2].classList.remove("valid"); 
                    passwordMessageItems[2].classList.add("invalid"); 
                } 

                // Checking length of the password 
                if (passwordInput.value.length >= 8) { 
                    passwordMessageItems[3].classList.remove("invalid"); 
                    passwordMessageItems[3].classList.add("valid"); 
                } else { 
                    passwordMessageItems[3].classList.remove("valid"); 
                    passwordMessageItems[3].classList.add("invalid"); 
                } 
            }
        } else {
            console.error("Password criteria message elements are missing.");
        }
    } else {
        console.error("One or more input fields are missing from the form.");
    }
});