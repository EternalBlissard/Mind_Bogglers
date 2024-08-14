// let allBooks = [
//     'The Alchemist',
//     'The Power of Now',
//     'The Four Agreements',
//     'The Art of War',
//     'The 48 Laws of Power',
//     'The Mastery of Love',
//     'The Subtle Art of Not Giving a F*ck',
//     'The 7 Habits of Highly Effective People',
//     'The Power of Habit',
//     'The 5 Love Languages',
//     'The Intelligent Investor',
// ]

const resultBox = document.querySelector('.result-box');
const inputBox = document.querySelector('#input-box');

inputBox.onkeyup = function() {
    let result = [];
    let input = inputBox.value;
    let search = inputBox.value.toLowerCase();
    if (search.length > 0) {
        result = allBooks.filter((keyword)=> {
           return keyword.toLowerCase().includes(search);
        });
        
    }
    displayResult(result);

    if (result.length === 0 && search.length > 0) {
        resultBox.innerHTML = '<span class="no-book">No such book</span>';
;
    }
}

function displayResult(result) {
    const content = result.map((book) => {
        return `<li>${book}</li>`;
    }).join('');

    resultBox.innerHTML = `<ul>${content}</ul>`;

    // Add event listener to each list item
    const listItems = document.querySelectorAll('.result-box ul li');
    listItems.forEach(item => {
        item.addEventListener('click', () => {
            inputBox.value = item.textContent;
            resultBox.innerHTML = '';            // Clear the result box after selection
        });
    });
    
}



// Hide suggestions when clicking outside the search box
document.addEventListener('click', function(event) {
    const isClickInside = inputBox.contains(event.target);
    const isClickInsideResultBox = resultBox.contains(event.target);

    if (!isClickInside && !isClickInsideResultBox) {
        resultBox.innerHTML = ''; // Clear the result box
    }
    
});

// Show suggestions when clicking inside the search box
inputBox.addEventListener('focus', function() {
    let search = inputBox.value.toLowerCase();
    if (search.length > 0) {
        let result = allBooks.filter((keyword) => {
            return keyword.toLowerCase().includes(search);
        });
        displayResult(result);
    }
});


const searchButton = document.querySelector('#search-button');

searchButton.addEventListener('click', () => {
    const query = inputBox.value.trim().toLowerCase();
    const bookExists = allBooks.some(book => book.toLowerCase() === query);

    if (bookExists) {
        window.location.href = `yourBook.html?search=${encodeURIComponent(query)}`;

    } else {
        const toastElement = document.getElementById('customToast');

        if (toastElement) { // Check if the element exists
            // Reset the toast visibility
            toastElement.style.opacity = '0';
            toastElement.style.display = 'block';

            // Force reflow to reset animation
            void toastElement.offsetWidth;

            // Show the toast
            toastElement.style.opacity = '1';

            // Add event listener to hide toast when closed
            toastElement.querySelector('.toastClose').addEventListener('click', () => {
                toastElement.style.display = 'none';
                console.log('Toast closed');
            });
            
        } else {
            console.error('Toast element not found');
        }
    }
});





function validateNumberInput(event) {
    const value = event.target.value;
    const sanitizedValue = value.replace(/[^0-9]/g, '');
    if (sanitizedValue === '' || parseInt(sanitizedValue, 10) < 1) {
        event.target.value = '';
    } else {
        event.target.value = sanitizedValue;
    }
}

document.getElementById('min-reviews-book').addEventListener('input', validateNumberInput);
document.getElementById('min-reviews-user').addEventListener('input', validateNumberInput);
document.getElementById('num-books-display').addEventListener('input', validateNumberInput);





// Get modal element
var modal = document.getElementById("bookModal");

// Get the images that open the modal
var images = document.querySelectorAll('.carousel-inner .item img');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("cardClose")[0];

// When the user clicks on an image, open the modal 
images.forEach(image => {
    image.onclick = function() {
        // Set book details
        document.getElementById("bookImage").src = this.src; // Set the book image
        document.getElementById("bookTitle").textContent = "Book Title"; // Customize as needed
        document.getElementById("bookAuthorName").textContent = "Author Name"; // Customize as needed
        document.getElementById("bookPublisherName").textContent = "Publisher Name"; // Customize as needed
        document.getElementById("bookYearPublished").textContent = "Year"; // Customize as needed
        
        modal.style.display = "flex"; // Center the modal using flex
    }
});

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}



