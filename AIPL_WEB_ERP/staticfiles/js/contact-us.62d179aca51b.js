  // Function to show the contact form
  function showContactForm() {
    document.getElementById('contactFormContainer').style.display = 'flex';
  }

  // Function to hide the contact form
  function hideContactForm() {
    document.getElementById('contactFormContainer').style.display = 'none';
  }

  // Prevent the form from submitting for demonstration purposes
  document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Handle form submission here

    hideContactForm(); // Hide the form after submission
  });