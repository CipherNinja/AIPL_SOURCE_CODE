// Smooth Scrolling for Sidebar Links
document.querySelectorAll('.privacy-sidebar a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Email Validation for Subscribe Button
document.getElementById('submit-btn').addEventListener('click', function() {
    var email = document.getElementById('email-input').value;
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    if (!emailPattern.test(email)) {
        alert('Please enter a valid email address.');
    } else {
        alert('Subscribed successfully!');
    }
});
