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
function showAlert() {
alert("¿Estás segura de que quieres cancelar?");
}

$(document).ready(function() {
  $('#createRoomModal').modal('show');
});
$(document).ready(function() {
  $('#exitRoomModal').modal('show');
});


window.addEventListener('DOMContentLoaded', () => {
    const idCardInput = document.getElementById('id_card');
    const idCardStatus = document.getElementById('id_card_status');

    idCardInput.addEventListener('input', function() {
      const idCardValue = idCardInput.value;
      fetch('/validate_id_card', {
        method: 'POST',
        body: JSON.stringify({ id_card: idCardValue }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          idCardStatus.innerHTML = data.message;
          idCardInput.classList.remove('invalid');
          idCardInput.classList.add('valid');
        } else {
          idCardStatus.innerHTML = data.message;
          idCardInput.classList.remove('valid');
          idCardInput.classList.add('invalid');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
});