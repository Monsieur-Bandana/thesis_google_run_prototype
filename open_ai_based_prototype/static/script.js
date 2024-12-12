const dynamicContent = document.getElementById('dynamic-content');
const buttonsdiv = document.getElementById('buttonContainer');
const inputField = document.getElementById('text-field');
let isOnButtonScreen = true;
const backButton = `
<button onclick="goBack()" style="display: block" class="return-button" id="backButton">Try other phone!</button>
`
const spinner = `<div id="loading-spinner" class="spinner"></div>`
const clock = document.getElementById('clock');
let hrs = document.getElementById("hrs");
let min = document.getElementById("min");

setInterval(() => {

    let currentTime = new Date();

    hrs.innerHTML = (currentTime.getHours() < 10 ? "0" : "") + currentTime.getHours();
    min.innerHTML = (currentTime.getMinutes() < 10 ? "0" : "") + currentTime.getMinutes();
}, 1000)

function flask_call(input) {
    dynamicContent.innerHTML = spinner;
    dynamicContent.style = 'height: 90%';
    clock.style = "display: none";
    isOnButtonScreen = false;
    fetch('/get-data', {
        method: 'POST', headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `input_text=${encodeURIComponent(input)}`,
    })
        .then(response => response.text()) // Parse the response as text (HTML)
        .then(htmlContent => {
            // Insert the fetched HTML into the DOM
            dynamicContent.innerHTML = backButton + htmlContent;
        })
        .catch(error => {
            console.error('Error fetching dynamic content:', error);
        });
}

function getButtons() {
    dynamicContent.innerHTML = spinner;
    fetch('/get-buttons').then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(responseList => {
        htmlEl = `<div style="width: 100%">Or choose from the provided list of buttons ... </div>`
        responseList.forEach(tuple => {
            htmlEl = htmlEl + `
                    <div class="buttonContent" name="${tuple['text']}">
                        <div>
    
                            <button class="eco-button" onclick="insertText('${tuple['text']}')">
                                <img src="${tuple['img']}">
                            </button>
                        </div>
                        <p class="button-text">${tuple['text']}</p>
                    </div>
    
                    `

        })

        dynamicContent.innerHTML = htmlEl;
    }).catch(error => {
        console.error('Error fetching data:', error);
    });
}

function goBack() {
    getButtons();
}


function insertText(buttonText) {
    const textField = document.getElementById("text-field");
    textField.value = buttonText;
    flask_call(buttonText);
}

inputField.addEventListener('input', function () {
    if (!isOnButtonScreen) {
        getButtons();
        isOnButtonScreen = true;
    }
});



// MutationObserver einrichten
const observer = new MutationObserver(() => {
    // Buttons erneut abrufen
    let buttons = document.querySelectorAll('#dynamic-content .buttonContent');
    console.log("Buttons gefunden:");
    console.log(buttons);

    // Optional: UI aktualisieren
    if (buttons.length > 0) {
        console.log(`Es wurden ${buttons.length} Buttons gefunden.`);
    }
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
});

// Observer konfigurieren und starten
observer.observe(dynamicContent, { childList: true, subtree: true });


const loadButton = document.getElementById('load-content-button');
const userInputField = document.getElementById('text-field');
loadButton.addEventListener('click', () => {
    // Fetch HTML content from the Flask API
    const inputval = userInputField.value;
    flask_call(inputval)
});

document.addEventListener("DOMContentLoaded", () => {
    getButtons();
})
