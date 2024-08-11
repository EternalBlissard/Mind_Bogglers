let allBooks = [
    'The Alchemist',
    'The Power of Now',
    'The Four Agreements',
    'The Art of War',
    'The 48 Laws of Power',
    'The Mastery of Love',
    'The Subtle Art of Not Giving a F*ck',
    'The 7 Habits of Highly Effective People',
    'The Power of Habit',
    'The 5 Love Languages',
    'The Intelligent Investor',
]

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
        console.log(result);
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
