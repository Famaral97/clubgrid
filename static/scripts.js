let clubs = []
let gridIds = []

let modalOverlay = ''
let extraModalOverlay = ''
let searchInput = ''
let dropdownContainer = ''
let gridContainer = ''

let conditions = {}

let gridAnswers
let guessesLeft

async function getData() {
    const url = "/clubs";
    await fetch(url) // Replace with the actual API URL
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

window.onload = async () => {
    await getData()
    getGridsIds()

    gridAnswersCookieValue = getCookie("grid_answers")

    gridAnswers = gridAnswersCookieValue ? JSON.parse(gridAnswersCookieValue) : [
        {}, {}, {},
        {}, {}, {},
        {}, {}, {}
    ]

    gridAnswers.forEach((gridAnswer, i) => {
        if (Object.keys(gridAnswer).length === 0) return
        const cell = document.getElementById(i + 1)

        console.log("loading answers")
        const club = clubs.filter(c => c.id === gridAnswer.id)[0]

        fillCell(cell, club.name, club.logo, gridAnswer.score)
    })

    guessesLeftCookieValue = getCookie("guessesLeft")
    guessesLeft = guessesLeftCookieValue ? parseInt(guessesLeftCookieValue) : 15

    document.getElementById("guesses").innerHTML = guessesLeft

    modalOverlay = document.querySelector('.modal-overlay')
    extraModalOverlay = document.querySelector('.modal-overlay-extra')
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

    conditions = {
        row: cell.getAttribute('rowCond'),
        column: cell.getAttribute('colCond')
    }

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

function exitModal(e) {
    if (e.target === modalOverlay) {
        hideModal()
    } else if (e.target === extraModalOverlay) {
        extraModalOverlay.style.display = 'none'
        document.querySelector(".solutions-modal").remove()
    }
}

function exitFinalMode(e) {
    if (e.target === modalOverlay) {
        modalOverlay.style.display = 'none'
        const viewResultsButton = document.querySelector('.view-results')
        viewResultsButton.style.display = 'block'
        viewResultsButton.onclick = () => modalOverlay.style.display = 'flex'
    }

    document.querySelectorAll('.container .grid-cell').forEach(cell => {
        cell.onclick = null
        cell.style.cursor = 'default'
    })
}

function hideModal() {
    hideAllModals()

    selectedCell = document.querySelector('.grid-cell.selected')
    if (selectedCell !== null) selectedCell.classList.remove('selected')

    conditions = {}

    modalOverlay.style.display = 'none'
    searchInput.value = '' // Clear search input
    dropdownContainer.innerHTML = '' // Clear previous dropdown options
}

// Function to filter and display clubs
function listOptions() {
    const searchString = searchInput.value.toLowerCase();
    dropdownContainer.innerHTML = '';

    if (searchString.length < 3) return

    const filteredClubs = clubs.filter(club => club.name.toLowerCase().includes(searchString));

    filteredClubs.forEach(club => {
        const optionContainer = document.createElement('div')
        optionContainer.className = 'dropdown-option'

        const clubName = document.createElement('span')
        clubName.textContent = club.name;

        const selectButton = document.createElement('button')
        if (gridAnswers.includes(club.id)) {
            optionContainer.classList.add('disabled')
            selectButton.disabled = true
        }
        selectButton.textContent = 'Select'
        selectButton.onclick = () => {
            submitClub(club.id)
        }

        optionContainer.appendChild(clubName)
        optionContainer.appendChild(selectButton)

        dropdownContainer.appendChild(optionContainer)
    });
}

async function submitClub(clubId) {
    const url = "/answer";

    const gridId = document.querySelector('.grid-title').getAttribute('gridId')

    let selectedCell = document.querySelector('.selected')
    fetch(url, {
        method: "POST", headers: {
            'Accept': 'application/json', "Content-Type": "application/json"
        }, body: JSON.stringify({
            "grid-id": gridId,
            "club-id": clubId,
            "row-condition-id": conditions.row,
            "column-condition-id": conditions.column
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Failed to check club');
        }
        return response.json();
    })
        .then(data => {
            if (data.correct) {
                let rarity_score = Math.floor(100 * data.total_club_answered / data.total_correct_answers)

                fillCell(selectedCell, data.clubName, data.logo, rarity_score)

                gridAnswers[selectedCell.id - 1] = {"id": clubId, "score": isNaN(rarity_score) ? 0 : rarity_score}
                document.cookie = `grid_answers=${JSON.stringify(gridAnswers)}; path=/grid/${gridId};`
            } else {
                applyPowEffect(selectedCell)
                selectedCell.animate(
                    [{backgroundColor: 'darkred', offset: 0.3}],
                    {duration: 1000, iterations: 1}
                );
            }

            hideModal()
            guessesLeft -= 1
            document.cookie = `guessesLeft=${guessesLeft}; path=/grid/${gridId};`

            document.getElementById("guesses").innerHTML = guessesLeft
            if (gridAnswers.filter(c => Object.keys(c).length !== 0).length == 9 || guessesLeft == 0) {
                showFinalModal()
            }

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

