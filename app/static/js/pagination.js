/*
=============================================================================
     Project: Game API App
     Developer: Varsha Rana
     File: pagination.js
     Description: This script manages the pagination, sorting, and filtering
                  of the character list within the web application. It handles
                  the display of a table showing character details such as name,
                  house, role, strength, animal, symbol, nickname, age, and death
                  status. The script supports dynamic pagination, enabling users
                  to navigate through multiple pages of characters. It also allows
                  users to filter characters based on various attributes (name,
                  house, role, strength, age) and change the sorting order of the
                  columns. Each character entry includes options to edit or delete
                  the character, with a confirmation prompt displayed before
                  deletion. The script ensures a responsive interface across
                  different screen sizes. Additionally, it uses AJAX to load new
                  pages without reloading the entire page, enhancing user experience.
     Created: 2024-12-02
     Updated: 2024-12-08
=============================================================================
*/

document.addEventListener('DOMContentLoaded', function () {
    // Select all pagination links
    const paginationLinks = document.querySelectorAll('.pagination .page-link');

    paginationLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent default link behavior

            // Get the target page number from the link
            const targetPage = parseInt(this.textContent) || null;
            const prevLink = this.closest('.page-item').previousElementSibling?.querySelector('.page-link');
            const nextLink = this.closest('.page-item').nextElementSibling?.querySelector('.page-link');

            // Prevent navigation on disabled links
            if (!targetPage && (this.closest('.page-item').classList.contains('disabled'))) return;

            let url = this.getAttribute('href'); // Get the page URL from the link's href attribute

            if (!url) {
                // Handle case for "Next" and "Previous" buttons
                if (prevLink && prevLink.textContent === 'Previous') {
                    url = prevLink.getAttribute('href');
                } else if (nextLink && nextLink.textContent === 'Next') {
                    url = nextLink.getAttribute('href');
                }
            }

            if (url) {
                // Fetch data for the new page
                fetch(url, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest', // Indicate that it's an AJAX request
                    },
                })
                    .then(response => response.text())
                    .then(data => {
                        // Use a DOMParser to safely extract the new table and pagination HTML
                        const parser = new DOMParser();
                        const newDoc = parser.parseFromString(data, 'text/html');

                        // Update the table and pagination controls
                        const newTable = newDoc.querySelector('#character-table');
                        const newPagination = newDoc.querySelector('#pagination-container-characters');

                        document.getElementById('character-table-container').innerHTML = newTable.outerHTML;
                        document.getElementById('pagination-container-characters').innerHTML = newPagination.outerHTML;
                    })
                    .catch(error => {
                        console.error('Error fetching page:', error);
                    });
            }
        });
    });
});
