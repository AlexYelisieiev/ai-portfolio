let languageFormsCount = 1;
let selectedLevels = {};

function addLanguageForm() {
    const languageFormsContainer = document.getElementById('languageFormsContainer');
    const newLanguageForm = document.createElement('div');
    newLanguageForm.className = 'language-form';
    const lang = document.createElement('input');
    lang.type = "text";
    lang.className = "lang-input"
    newLanguageForm.appendChild(lang);
    for (let i = 1; i <= 5; i++) {
        const oval = document.createElement('div');
        oval.className = 'rectangle';
        oval.onclick = () => setLanguageLevel(i, newLanguageForm);
        newLanguageForm.appendChild(oval);
    }

    languageFormsContainer.appendChild(newLanguageForm);
    selectedLevels[languageFormsCount] = 0;
    languageFormsCount++;
    colorRectangles(newLanguageForm);
}

function setLanguageLevel(level, form) {
    const formIndex = Array.from(form.parentNode.children).indexOf(form) + 1;
    selectedLevels[formIndex] = level;
    colorRectangles(form);
}

function colorRectangles(form) {
    const formIndex = Array.from(form.parentNode.children).indexOf(form) + 1;
    const selectedLevel = selectedLevels[formIndex];
    const rectangles = form.querySelectorAll('.rectangle');

    rectangles.forEach((rectangle, index) => {
        if (index < selectedLevel) {
            rectangle.style.backgroundColor = 'green';
        } else {
            rectangle.style.backgroundColor = 'lightgray';
        }
    });
}

function loadPage(pageName) {
        var contentContainer = document.getElementById('content');
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    contentContainer.innerHTML = xhr.responseText;
                } else {
                    console.error('Ошибка загрузки страницы: ' + xhr.status);
                }
            }
        };
        xhr.open('GET', '/load_page/' + pageName + '/', true);
        xhr.send();
    }