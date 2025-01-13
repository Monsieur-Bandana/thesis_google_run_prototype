const dynamicContent = document.getElementById('dynamic-content');
const buttonsdiv = document.getElementById('buttonContainer');
const inputField = document.getElementById('text-field');
const introText = document.getElementById('introductionText');
const list_of_tops_and_worst = document.getElementById('top-frame')
let isOnButtonScreen = true;
const backButton = `
<button onclick="goBack()" style="display: block" class="return-button" id="backButton">Try other phone!</button>
`
const spinner = `<div id="loading-spinner" class="spinner"></div>`

const introductionContainer = `
`;
const bestButtons = document.getElementById('best_phones');
const worstButtons = document.getElementById('worst_phones');
const dropL = document.getElementById('drop_content')
let allButtons = [];

function flask_call(input) {
    dynamicContent.innerHTML = "<div style='width: 100%'>Text will be generated. This can take up to 1 minute.<p></p></div>" + spinner;
    dynamicContent.style = 'display: block';
    introText.style.display = "none";

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

function getButtons2() {
    dynamicContent.innerHTML = spinner;
    fetch('/get-buttons').then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(responseList => {
        htmlEl = ``
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

function getButtons() {
    dynamicContent.innerHTML = spinner;
    return fetch('/get-buttons').then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(responseList => {


        return responseList;
    }).catch(error => {
        console.error('Error fetching data:', error);
    });
}

function executeGetSelButtons(type_, txt_) {
    fetch('/get-selected-buttons', {
        method: 'POST', headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `input_text=${encodeURIComponent(
            type_
        )}`,
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(responseList => {
        htmlEl = `<p>${txt_}</p>`
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
        if (type_ == "best") {

            bestButtons.innerHTML = htmlEl;
        } else {
            worstButtons.innerHTML = htmlEl
        }


    }).catch(error => {
        console.error('Error fetching data:', error);
    });
}

function getSelectedButtons() {
    bestButtons.innerHTML = spinner;
    worstButtons.innerHTML = spinner;
    executeGetSelButtons("best", "Phones with the lowest environmental footpint (best phones)");
    executeGetSelButtons("worst", "Phones with the highest environmental footpint (worst phones)");
}

function goBack() {
    getButtons();
}

function deactivate_other_els() {
    list_of_tops_and_worst.style = "display: none";
    introText.style = "display: none";
}

function load_all_buttons() {
    dynamicContent.style = "display: flex";
    deactivate_other_els()
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

const observer2 = new MutationObserver(() => {
    // Buttons erneut abrufen
    let buttons = allButtons
    allButtons.forEach(b => {
        dropL.add(`<li>${b["text"]}</li>`)
    })



    // Optional: UI aktualisieren
    if (buttons.length > 0) {
        console.log(`Es wurden ${buttons.length} Buttons gefunden.`);
    }
    inputField.addEventListener('input', function () {
        const filterText = inputField.value.toLowerCase();

        buttons.forEach(button => {
            if (button["text"].toLowerCase().includes(filterText)) {
                button.classList.remove('hidden');
            } else {
                button.classList.add('hidden');
            }
        });
    });
});


// MutationObserver einrichten
const observer = new MutationObserver(() => {
    // Buttons erneut abrufen
    let buttons = document.querySelectorAll('#dynamic-content .buttonContent');


    // Optional: UI aktualisieren
    if (buttons.length > 0) {
        console.log(`Es wurden ${buttons.length} Buttons gefunden.`);
    }
    inputField.addEventListener('input', function () {
        const filterText = inputField.value.toLowerCase();

        buttons.forEach(button => {
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
    allButtons = getButtons();
    getSelectedButtons();
    console.log(allButtons)
})
