document.addEventListener('DOMContentLoaded', function() {
    const encodeForm = document.getElementById('steganographyForm');

    encodeForm.addEventListener('submit', function(event) {
        // Get the message textarea element
        const messageInput = document.getElementById('message');
        
        // Check if the message is empty
        if (messageInput.value.trim() === '') {
            // Prevent form submission
            event.preventDefault();

            // Display an error message
            alert('Please enter a message.');
        }
    });
});
