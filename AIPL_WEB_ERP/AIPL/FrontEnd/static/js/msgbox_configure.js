// Adjust padding and top for success and error messages
window.onload = function() {

    // This function will hide the messages after 3 seconds
    setTimeout(function() {
        // Select all elements with class 'success' and 'error'
        var messages = document.querySelectorAll('.success, .error');
        messages.forEach(function(message) {
            // Start fading out the message
            message.style.transition = 'opacity 1s ease';  // Adds a fade-out transition
            message.style.opacity = '0';  // Set opacity to 0 to begin fading

            // Remove the message from the DOM after the fade-out transition completes
            setTimeout(function() {
                message.remove();
            }, 1000);  // Delay for 1 second (after the fade-out transition)
        });
    }, 3000);  // Wait for 3 seconds before starting the fade-out
};
