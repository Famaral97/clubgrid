let clubs = []

let modalOverlay = ''
let searchInput = ''
let dropdownContainer = ''
let gridContainer = ''

let conditions = []

let used_clubs = []
let guesses_left = 10

async function getData() {
    const url = "/clubs";
    fetch(url) // Replace with the actual API URL
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch clubs');
            }
            return response.json();
        })
        .then(data => {
            clubs = data
        })
        .catch(error => {
            console.error('Error fetching clubs:', error);
        });
}


window.onload = () => {
    getData();
    console.log(clubs)

    document.getElementById("guesses").innerHTML = guesses_left

    modalOverlay = document.querySelector('.modal-overlay');
    searchInput = document.querySelector('.search-input');
    dropdownContainer = document.querySelector('.dropdown-container');
    gridContainer = document.querySelector('.grid-container');
};

// Function to show modal
function showModal(cell) {
    cell.classList.add('selected')

    conditions = [cell.getAttribute('rowCond'), cell.getAttribute('colCond')]

    modalOverlay.style.display = 'flex';
    searchInput.focus(); // Focus on the input field for better user experience
}

function exitSubmitMode(e) {
    if (e.target === modalOverlay) {
        hideModal();
    }
}

// Function to hide modal
function hideModal() {

    document.querySelector('.grid-cell.selected').classList.remove('selected')
    conditions = []

    modalOverlay.style.display = 'none';
    searchInput.value = ''; // Clear search input
    dropdownContainer.innerHTML = ''; // Clear previous dropdown options
}

// Function to filter and display clubs
function listOptions() {
    const searchString = searchInput.value.toLowerCase();

    if (searchString.length < 3) return

    dropdownContainer.innerHTML = ''; // Clear previous results

    const filteredClubs = clubs.filter(club => club.name.toLowerCase().includes(searchString));

    filteredClubs.forEach(club => {
        const optionContainer = document.createElement('div');
        optionContainer.className = 'dropdown-option';

        // Club name
        const clubName = document.createElement('span');
        clubName.textContent = club.name;

        // Select button
        const selectButton = document.createElement('button');
        if (used_clubs.includes(club.name)) {
            optionContainer.classList.add('disabled')
            selectButton.disabled = true
        }
        selectButton.textContent = 'Select';
        selectButton.onclick = () => {

            submitClub(club.id).then( () => {
                console.log(club.name)
                hideModal()
                guesses_left -= 1
                document.getElementById("guesses").innerHTML = guesses_left
                if (used_clubs.length == 9) {
                    alert("Congratulations! You won!")
                } else if (guesses_left == 0) {
                    alert("You lost 😭")
                }
            })
        }

        // Append to option container
        optionContainer.appendChild(clubName);
        optionContainer.appendChild(selectButton);

        dropdownContainer.appendChild(optionContainer);
    });
}


async function submitClub(clubId) {
    console.log(conditions)
    const url = "/answer";
    let selectedCell = document.querySelector('.selected')
    fetch(url, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "club-id": clubId,
            "condition-id-1": conditions[0],
            "condition-id-2": conditions[1]
        })
    }).then(response => {
            if (!response.ok) {
                throw new Error('Failed to check club');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.correct) {
                selectedCell.style.backgroundImage = `url(${data.logo})`
                selectedCell.style.cursor = 'default'
                used_clubs.push(data.clubName)
                selectedCell.onclick = null
            }
            else {
                applyPowEffect(selectedCell)
            }
                // selectedCell.animate(
                //     [
                //       { backgroundColor: 'red', offset: 0.3 },
                //     ], {
                //       duration: 2000,
                //       iterations: 1
                //     }
                // );
        });
}

function applyPowEffect(cell) {
    cell.innerHTML = '';

    const powContainer = document.createElement('div');
    powContainer.classList.add('pow-container');
    cell.appendChild(powContainer);

    const powText = document.createElement('div');
    powText.classList.add('pow-text');
    powText.textContent = 'WRONG!';
    powContainer.appendChild(powText);

    setTimeout(() => {
        cell.innerHTML = ''; // Clear the cell content
    }, 1000); // Match the animation duration
}


