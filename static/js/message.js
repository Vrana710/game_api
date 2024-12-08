/*
=============================================================================
     Project: Game API App
     Developer: Varsha Rana
     File: message.js
     Description: This script manages the display of success messages within
                  the web application. It automatically hides success messages
                  after a set delay (e.g., 2 seconds), providing a smoother user
                  experience by removing them from the UI. The script specifically
                  targets elements with the `.alert-success` class, changing their
                  opacity and display to gradually hide them. This functionality is
                  particularly useful for showing brief notifications, such as
                  successful actions (e.g., character updates or deletions), without
                  cluttering the interface. The script ensures the application remains
                  clean and responsive by hiding notifications after a brief period.
     Created: 2024-12-02
     Updated: 2024-12-08
=============================================================================
*/


document.addEventListener('DOMContentLoaded', function () {
    // Automatic removal of success messages after a delay
    setTimeout(function () {
        const successMessages = document.querySelectorAll('.alert-success');
        successMessages.forEach(function (message) {
            message.style.opacity = 0;
            message.style.display = 'none';
        });
    }, 2000); // Adjust the timing (5000ms = 5 seconds) as needed
});
