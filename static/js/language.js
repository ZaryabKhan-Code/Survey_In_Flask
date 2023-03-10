function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,es',
        layout: google.translate.TranslateElement.InlineLayout.HORIZONTAL,
        autoDisplay: false,
        gaTrack: true,
        gaId: 'UA-12345-6'
    }, 'google_translate_element');
}

function changeLanguage(lang) {
    var select = document.querySelector("#google_translate_element select");
    var event = new Event("change");
    select.value = lang;
    select.dispatchEvent(event);
}