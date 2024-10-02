let clubs = []
let gridIds = []

let modalOverlay = ''
let searchInput = ''
let dropdownContainer = ''
let gridContainer = ''

let conditions = []

let used_clubs = []
let guesses_left = 15

async function getData() {
    const url = "/clubs";
    fetch(url) // Replace with the actual API URL
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch clubs');
            }
            return response.json()
        })
        .then(data => {
            clubs = data
        })
        .catch(error => {
            console.error('Error fetching clubs:', error);
        });
}

async function getGridsIds() {
    fetch("/grids").then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch grids');
        }
        return response.json()
    })
        .then(data => {
            gridIds = data
        })
        .catch(error => {
            console.error('Error fetching grids:', error);
        });
}

async function getGridSolution(gridId) {
    return fetch(`/grid/${gridId}/end`).then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch grids');
        }
        return response.json()
    })
        .then(data => {
            return data
        })
        .catch(error => {
            console.error('Error fetching grids:', error);
        });
}

window.onload = () => {
    getData()
    getGridsIds()

    document.getElementById("guesses").innerHTML = guesses_left

    modalOverlay = document.querySelector('.modal-overlay')
    searchInput = document.querySelector('.search-input')
    dropdownContainer = document.querySelector('.dropdown-container')
    gridContainer = document.querySelector('.grid-container')
};

function hideAllModals() {

    for (const child of modalOverlay.children) {
        child.style.display = 'none'
    }
}

function showGridSelectionModal() {
    hideAllModals()

    modalOverlay.style.display = 'flex'

    gridSelectionModal = document.createElement("div")
    gridSelectionModal.classList.add("grid-selection-modal")

    gridSelectionModalContainer = document.createElement("div")

    gridIds.forEach(gridId => {
        const gridOptionContainer = document.createElement('div')
        gridOptionContainer.className = 'dropdown-option'

        const gridName = document.createElement('span')
        gridName.textContent = `Grid #${gridId}`

        const selectGridButton = document.createElement('button')

        selectGridButton.textContent = 'Play!'
        selectGridButton.onclick = () => {
            location.replace(`/grid/${gridId}`)
        }

        gridOptionContainer.appendChild(gridName)
        gridOptionContainer.appendChild(selectGridButton)

        gridSelectionModalContainer.appendChild(gridOptionContainer)
    })

    gridSelectionModal.appendChild(gridSelectionModalContainer)

    modalOverlay.appendChild(gridSelectionModal)

}

function showInfoModal() {
    hideAllModals()

    modalOverlay.style.display = 'flex'

    let infoModal = displayInfo()

    modalOverlay.appendChild(infoModal)
}

function showClubSelectionModal(cell) {

    cell.classList.add('selected')

    conditions = [cell.getAttribute('rowCond'), cell.getAttribute('colCond')]

    modalOverlay.style.display = 'flex'
    modalOverlay.querySelector(".club-selection-modal").style.display = 'flex'
    searchInput.focus() // Focus on the input field for better user experience
}

async function showFinalModal() {
    hideAllModals()

    modalOverlay.style.display = 'flex'

    const gridId = document.querySelector('.grid-title').getAttribute('gridId')

    const {solutions, row_conditions_descriptions, col_conditions_descriptions} = await getGridSolution(gridId)

    finalModal = document.createElement("div")

    makeGrid(finalModal, solutions, row_conditions_descriptions, col_conditions_descriptions)

    finalModal.classList.add("final-modal")

    modalOverlay.appendChild(finalModal)
    modalOverlay.onclick = exitFinalMode
}

function exitSubmitMode(e) {
    if (e.target === modalOverlay) {
        hideModal()
    }
}

function exitFinalMode(e) {
    if (e.target === modalOverlay) {
        modalOverlay.style.display = 'none'
        const viewResultsButton = document.querySelector('.view-results')
        viewResultsButton.style.display = 'block'
        viewResultsButton.onclick = () => modalOverlay.style.display = 'flex'
    }

    document.querySelectorAll('.grid-cell').forEach(cell => {
        cell.onclick = null
        cell.style.cursor = 'default'
    })
}

// Function to hide modal
function hideModal() {
    hideAllModals()

    selectedCell = document.querySelector('.grid-cell.selected')
    if (selectedCell !== null) selectedCell.classList.remove('selected')

    conditions = []

    modalOverlay.style.display = 'none'
    searchInput.value = '' // Clear search input
    dropdownContainer.innerHTML = '' // Clear previous dropdown options
}

// Function to filter and display clubs
function listOptions() {
    const searchString = searchInput.value.toLowerCase();

    if (searchString.length < 3) return

    dropdownContainer.innerHTML = ''; // Clear previous results

    const filteredClubs = clubs.filter(club => club.name.toLowerCase().includes(searchString));

    filteredClubs.forEach(club => {
        const optionContainer = document.createElement('div')
        optionContainer.className = 'dropdown-option'

        // Club name
        const clubName = document.createElement('span')
        clubName.textContent = club.name;

        // Select button
        const selectButton = document.createElement('button')
        if (used_clubs.includes(club.name)) {
            optionContainer.classList.add('disabled')
            selectButton.disabled = true
        }
        selectButton.textContent = 'Select'
        selectButton.onclick = () => {
            submitClub(club.id)
        }

        // Append to option container
        optionContainer.appendChild(clubName)
        optionContainer.appendChild(selectButton)

        dropdownContainer.appendChild(optionContainer)
    });
}

async function submitClub(clubId) {
    const url = "/answer";
    let selectedCell = document.querySelector('.selected')
    fetch(url, {
        method: "POST", headers: {
            'Accept': 'application/json', "Content-Type": "application/json"
        }, body: JSON.stringify({
            "club-id": clubId, "condition-id-1": conditions[0], "condition-id-2": conditions[1]
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Failed to check club');
        }
        return response.json();
    })
        .then(data => {
            if (data.correct) {
                selectedCell.style.backgroundImage = `url(${data.logo})`
                selectedCell.style.cursor = 'default'
                used_clubs.push(data.clubName)
                selectedCell.onclick = null
            } else {
                applyPowEffect(selectedCell)
            }

            hideModal()
            guesses_left -= 1
            document.getElementById("guesses").innerHTML = guesses_left
            if (used_clubs.length == 9 || guesses_left == 0) {
                showFinalModal()
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


