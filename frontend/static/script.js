const dynamicContent = document.getElementById('dynamic-content');
const buttonsdiv = document.getElementById('buttonContainer');
const inputField = document.getElementById('text-field');
const introText = document.getElementById('introductionText');
const list_of_tops_and_worst = document.getElementById('top-frame')
let isOnButtonScreen = true;

const spinner = `<div style="display: block; width: 100%"><div id="loading-spinner" class="spinner"></div></div>`

const introductionContainer = `
`;
const bestButtons = document.getElementById('best_phones');
const worstButtons = document.getElementById('worst_phones');
const dropF = document.getElementById('drop_content_fr');
const dropL = document.getElementById('drop_content');
const headm = document.getElementById('head_menu');
const seeAllBottom = document.getElementById('bottomSeeAll');
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
            dynamicContent.innerHTML = htmlContent;
        })
        .catch(error => {
            console.error('Error fetching dynamic content:', error);
        });
}

function createButton(tuple) {
    return `
                    <div class="buttonContent" name="${tuple['text']}">
                        <div>
    
                            <button class="eco-button" onclick="insertText('${tuple['text']}')">
                                <img src="${tuple['img']}">
                            </button>
                        </div>
                        <p class="button-text">${tuple['text']}</p>
                    </div>
    
                    `;
}

function getButtons2() {
    dynamicContent.innerHTML = spinner;
    let htmlEl = '';
    console.log(allButtons);
    console.log(typeof allButtons);
    console.log(Array.isArray(allButtons));
    allButtons.forEach(tuple => {
        htmlEl = htmlEl + createButton(tuple);

    });


    dynamicContent.innerHTML = htmlEl;

}

function getButtons() {
    // dynamicContent.innerHTML = spinner;
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
            htmlEl = htmlEl + createButton(tuple);

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
    render_main_screen();
}

function deactivate_other_els() {
    list_of_tops_and_worst.style = "display: none";
    introText.style = "display: none";
    headm.style = "display: flex";
    seeAllBottom.style = "display: none";
    dynamicContent.style = "display: flex";

}

const searchContainer = document.getElementById("sc");
function render_load_animation() {
    list_of_tops_and_worst.style = "display: none";
    introText.style = "display: none";
    headm.style = "display: none";
    seeAllBottom.style = "display: none";
    dynamicContent.style = "display: flex; height: 100%; width: 100%; justify-content: center; flex-direction: column";
    dynamicContent.innerHTML = spinner;
    searchContainer.style = "display: none";
}

function render_main_screen() {
    list_of_tops_and_worst.style = "display: block";
    introText.style = "display: block";
    headm.style = "display: none";
    seeAllBottom.style = "display: block";
    dynamicContent.style = "display: none";
    searchContainer.style = "display: flex";
}

function load_all_buttons() {
    deactivate_other_els()
    getButtons2();
}


function insertText(buttonText) {
    const textField = document.getElementById("text-field");
    textField.value = buttonText;
    flask_call(buttonText);
    deactivate_other_els()
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
        dropF.style = display.block;
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
observer2.observe(dynamicContent, { childList: true, subtree: true });


const loadButton = document.getElementById('load-content-button');
const userInputField = document.getElementById('text-field');
loadButton.addEventListener('click', () => {
    // Fetch HTML content from the Flask API
    const inputval = userInputField.value;
    flask_call(inputval)
});

document.addEventListener("DOMContentLoaded", async () => {
    render_load_animation();
    allButtons = await getButtons();
    render_main_screen();
    getSelectedButtons();
    headm.style = "display: none";
    console.log(allButtons)
})
