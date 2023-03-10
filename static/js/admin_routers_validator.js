const emailInput = document.getElementById('email-registration');
const emailInputerrorMessage = document.getElementById('email-error-message');
emailInput.addEventListener('input', async () => {
    const response = await fetch(`/check_email/${emailInput.value}`);
    const result = await response.json();
    if (result.error) {
      emailInputerrorMessage.textContent = result.error;
    } else {
        emailInputerrorMessage.textContent = '';
    }
  });

  const usernameInput = document.getElementById('username-registration');
  const usernameInputerrorMessage = document.getElementById('username-error-message');
  usernameInput.addEventListener('input', async () => {
      const response = await fetch(`/check_username/${usernameInput.value}`);
      const result = await response.json();
      if (result.error) {
        usernameInputerrorMessage.textContent = result.error;
      } else {
        usernameInputerrorMessage.textContent = '';
      }
    });


    function searchTable() {
		// Declare variables
		var input, filter, table, tr, td, i, txtValue;
		input = document.getElementById("searchInput");
		filter = input.value.toUpperCase();
		table = document.getElementById("dataTable");
		tr = table.getElementsByTagName("tr");

		// Loop through all table rows, and hide those that don't match the search query
		for (i = 0; i < tr.length; i++) {
			td = tr[i].getElementsByTagName("td");
			for (var j = 0; j < td.length; j++) {
				if (td[j]) {
					txtValue = td[j].textContent || td[j].innerText;
					if (txtValue.toUpperCase().indexOf(filter) > -1) {
						tr[i].style.display = "";
						break;
					} else {
						tr[i].style.display = "none";
					}
				}
			}
		}
	}
