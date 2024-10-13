document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    // Get input values
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const linkedin = document.getElementById('linkedin').value;
    const github = document.getElementById('github').value;

    // Validation checks
    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return; // Stop submission if email is invalid
    }

    if (!validatePhone(phone)) {
        alert('Please enter a valid 10-digit phone number.');
        return; // Stop submission if phone is invalid
    }

    if (linkedin && !validateURL(linkedin)) {
        alert('Please enter a valid LinkedIn URL.');
        return; // Stop submission if LinkedIn URL is invalid
    }

    if (github && !validateURL(github)) {
        alert('Please enter a valid GitHub URL.');
        return; // Stop submission if GitHub URL is invalid
    }

    // If all validations pass
    alert('Form Submitted Successfully!');
});

// Email validation
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email format
    return emailPattern.test(email);
}

// Phone number validation (10 digits)
function validatePhone(phone) {
    const phonePattern = /^[0-9]{10}$/; // 10 digit number
    return phonePattern.test(phone);
}

// URL validation (checks for http:// or https://)
function validateURL(url) {
    const urlPattern = /^(http|https):\/\/[^\s$.?#].[^\s]*$/; // Basic URL format
    return urlPattern.test(url);
}
