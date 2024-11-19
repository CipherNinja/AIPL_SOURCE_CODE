// Handling the contact form submission
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Your message has been sent!');
});


const hamburgerIcon = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

// Toggle menu visibility and hamburger icon
hamburgerIcon.addEventListener('click', function(event) {
    navLinks.classList.toggle('show');
    
    // Stop the click from propagating (so it doesn't trigger the document listener)
    event.stopPropagation();
});

// Close menu and show hamburger icon when clicking outside
document.addEventListener('click', function(event) {
    // Check if the menu is open and the click is outside the menu and hamburger icon
    if (navLinks.classList.contains('show') && !navLinks.contains(event.target) && !hamburgerIcon.contains(event.target)) {
        navLinks.classList.remove('show'); // Hide the menu
    }
});

  
  document.getElementById('search-button').addEventListener('click', function() {
    const searchBox = document.getElementById('search-box');
    if (searchBox.style.display === 'block') {
        searchBox.style.display = 'none';
    } else {
        searchBox.style.display = 'block';
    }
  });
  
  // Hide search box when clicking outside
  document.addEventListener('click', function(event) {
    const searchBox = document.getElementById('search-box');
    const searchButton = document.getElementById('search-button');
    if (!searchButton.contains(event.target) && !searchBox.contains(event.target)) {
        searchBox.style.display = 'none';
    }
  });
  