const dynamicContent = document.getElementById('dynamic-content');

function flask_call(input) {
    fetch('/get-data', {
        method: 'POST', headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `input_text=${encodeURIComponent(input)}`,
    })
        .then(response => response.text()) // Parse the response as text (HTML)
        .then(htmlContent => {
            // Insert the fetched HTML into the DOM
            dynamicContent.innerHTML = htmlContent;
        })
        .catch(error => {
            console.error('Error fetching dynamic content:', error);
        });
}


function insertText(buttonText) {
    const textField = document.getElementById("text-field");
    textField.value = buttonText;

    flask_call(buttonText);
}

let hrs = document.getElementById("hrs")
let min = document.getElementById("min")

setInterval(() => {

    let currentTime = new Date();

    hrs.innerHTML = (currentTime.getHours() < 10 ? "0" : "") + currentTime.getHours();
    min.innerHTML = (currentTime.getMinutes() < 10 ? "0" : "") + currentTime.getMinutes();
}, 1000)


const inputField = document.getElementById('text-field');
const buttons = document.querySelectorAll('#buttonContainer .buttonContent');

inputField.addEventListener('input', function () {
    const filterText = inputField.value.toLowerCase();
    buttons.forEach(button => {
        console.log(button.textContent)
        if (button.textContent.toLowerCase().includes(filterText)) {
            button.classList.remove('hidden');
        } else {
            button.classList.add('hidden');
        }
    });
});

const loadButton = document.getElementById('load-content-button');
const userInputField = document.getElementById('text-field');
loadButton.addEventListener('click', () => {
    // Fetch HTML content from the Flask API
    const inputval = userInputField.value;
    flask_call(inputval)
});