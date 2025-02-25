const inputField = document.getElementById('text-field');
const introText = document.getElementById('introductionText');
let isOnButtonScreen = true;

const spinner = `<div style="display: block; width: 100%"><div id="loading-spinner" class="spinner"></div></div>`
const logoHeader = document.getElementById('logo_header');

const introductionContainer = `
`;
const bestButtons = document.getElementById('best_phones');
const worstButtons = document.getElementById('worst_phones');
const dropF = document.getElementById('drop_content_fr');
const dropL = document.getElementById('drop_content');
let allButtons = [];

function flask_call(input, mode = "") {
    const locDynamicContent = document.getElementById(`dynamic-content`);
    deactivate_other_els();
    locDynamicContent.innerHTML = "<div style='width: 100%'>Text will be generated. This can take up to 1 minute.<p></p></div>" + spinner;
    locDynamicContent.style = 'display: block';
    introText.style.display = "none";

    isOnButtonScreen = false;
    fetch('/get-data', {
        method: 'POST', headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `input_text=${encodeURIComponent(`${input},${mode}`)}`,
    })
        .then(response => response.text()) // Parse the response as text (HTML)
        .then(htmlContent => {
            // Insert the fetched HTML into the DOM
            locDynamicContent.innerHTML = htmlContent;
        })
        .catch(error => {
            console.error('Error fetching dynamic content:', error);
        });
    document.getElementById('compareButton').style = "display: block";

    if (mode == "2") {

        document.getElementById(`compare_menu`).style = "display: none";
    }
}

function createButton(tuple, mode = "") {
    extension = ""
    if (tuple["text"].includes("Fairphone")) {
        extension = `style="filter: invert(1);"`
    }
    return `
    <div class="buttonContent" name="${tuple['text']}">
    <div>
    
    <button class="eco-button" onclick="insertText('${tuple['text']}', ${mode})">
    <img src="${tuple['img']}" ${extension}>
    </button>
    </div>
    <p class="button-text">${tuple['text']}</p>
                    </div>
                    
                    `;
}

function getButtons2(filter = "", mode = "") {
    const locDynamicContent = document.getElementById(`dynamic-content${mode}`);
    locDynamicContent.innerHTML = spinner;
    let htmlEl = '';
    console.log(allButtons);
    console.log(typeof allButtons);
    console.log(Array.isArray(allButtons));
    const filteredButtons = allButtons.filter(b =>
        b.text.toLowerCase().includes(filter.toLowerCase())
    );
    filteredButtons.forEach(tuple => {
        htmlEl = htmlEl + createButton(tuple, mode);

    });


    locDynamicContent.innerHTML = htmlEl;

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

function goBack(mode = "") {
    render_main_screen(mode);
}


function deactivate_other_els(mode = "") {
    const locBrandsFrame = document.getElementById(`brands_frame${mode}`);
    const locDynamicContent = document.getElementById(`dynamic-content${mode}`);
    if (mode != "2") {

        const locHeadm = document.getElementById(`head_menu${mode}`);
        locHeadm.style = "display: flex; margin-top: 20px";
    }
    const locList_of_tops_and_worst = document.getElementById(`top-frame${mode}`);
    const locSeeAllBottom = document.getElementById(`bottomSeeAll${mode}`);
    locList_of_tops_and_worst.style = "display: none";
    introText.style = "display: none";
    locSeeAllBottom.style = "display: none";
    locDynamicContent.style = "display: flex";
    drop_content_fr.style = "display: none";
    locBrandsFrame.style = "display: none";
    logoHeader.style = "display: none";
}

const searchContainer = document.getElementById("sc");
function render_load_animation(mode = "") {
    deactivate_other_els(mode);
    const locHeadm = document.getElementById(`head_menu${mode}`);
    const locDynamicContent = document.getElementById(`dynamic-content${mode}`);
    const locearchContainer = document.getElementById(`sc${mode}`);
    locHeadm.style = "display: none";
    locDynamicContent.style = "display: flex; height: 100%; width: 100%; justify-content: center; flex-direction: column";
    locDynamicContent.innerHTML = spinner;
    locearchContainer.style = "display: none";
}

function render_main_screen(mode = "") {
    const locBrandsFrame = document.getElementById(`brands_frame${mode}`);
    const locList_of_tops_and_worst = document.getElementById(`top-frame${mode}`);
    const locDynamicContent = document.getElementById(`dynamic-content${mode}`);
    const locearchContainer = document.getElementById(`sc${mode}`);
    const locSeeAllBottom = document.getElementById(`bottomSeeAll${mode}`);
    locBrandsFrame.style = "display: flex"
    locList_of_tops_and_worst.style = "display: block";
    if (mode != "2") {
        const locHeadm = document.getElementById(`head_menu${mode}`);
        introText.style = "display: block";
        logoHeader.style = "display: flex";
        locHeadm.style = "display: none";
    }
    locSeeAllBottom.style = "display: block";
    locDynamicContent.style = "display: none";
    locearchContainer.style = "display: flex";
}

function load_all_buttons(filter = "", mode = "") {
    deactivate_other_els(mode)
    getButtons2(filter, mode);
}


function insertText(buttonText, mode = "") {
    const textField = document.getElementById(`text-field${mode}`);
    textField.value = buttonText;
    flask_call(buttonText, mode);
}

function compare_action() {
    document.getElementById('compare_menu').style = "display: flex";
    render_main_screen("2")
}

function end_compare_action() {
    document.getElementById('mobile2').style = "display: none";
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
modedef = ""
const dynamicContent = document.getElementById(`dynamic-content${modedef}`);
observer.observe(dynamicContent, { childList: true, subtree: true });

function generateDropList(filteredButtons) {
    li_els = ""
    filteredButtons.forEach(b => {
        li_els = li_els + `<li onclick="insertText('${b['text']}')">${b["text"]}</li>`;
    })
    dropL.innerHTML = li_els;
}

function filterDropList(inputValue) {
    const filteredButtons = allButtons.filter(b =>
        b.text.toLowerCase().includes(inputValue.toLowerCase())
    );
    generateDropList(filteredButtons); // Generiere Dropdown mit gefilterten Elementen
}

document.addEventListener('DOMContentLoaded', () => {
    generateDropList(allButtons);

    // Eventlistener für Benutzereingabe
    inputField.addEventListener('input', (event) => {
        const inputValue = event.target.value;
        drop_content_fr.style = "display: flex"
        filterDropList(inputValue); // Filtere die Liste basierend auf Eingabe
    });
});

const dropwdown_observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        if (mutation.type === 'childList') {
            console.log('Dropdown updated:', mutation);
        }
    });
});

document.addEventListener('click', (event) => {
    const isClickInsideInput = inputField.contains(event.target);
    const isClickInsideDropdown = dropL.contains(event.target);

    if (!isClickInsideInput && !isClickInsideDropdown) {
        dropL.style.display = 'none'; // Hide the dropdown
    }
});

// Show dropdown when the input field is focused
inputField.addEventListener('focus', () => {
    dropL.style.display = 'block'; // Show the dropdown
});

dropwdown_observer.observe(dropL, { childList: true });

const loadButton = document.getElementById('load-content-button');
const userInputField = document.getElementById('text-field');
loadButton.addEventListener('click', () => {
    // Fetch HTML content from the Flask API
    const inputval = userInputField.value;
    flask_call(`${inputval},${mode}`)
});

const headm = document.getElementById('head_menu');
document.addEventListener("DOMContentLoaded", async () => {
    render_load_animation();
    allButtons = await getButtons();
    render_main_screen();
    getSelectedButtons();
    headm.style = "display: none";
    console.log(allButtons)
})
