const GUESSES_NUMBER = 12

let clubs = []
let grids = []

// modals
let modalOverlay = ''
let extraModalOverlay = ''
let searchInput = ''
let dropdownContainer = ''
let gridContainer = ''

// current grid
let conditions = {}
let gridAnswers
let allGuesses
let currentGridId
let gridScore

window.onload = async () => {
    await getData()
    getGrids()

    currentGridId = document.querySelector('.grid-title').getAttribute('gridId')

    let gridScoreStoredValue = parseFloat(window.localStorage.getItem(`gridScore_${currentGridId}`))
    gridScore = gridScoreStoredValue || 0

    let gridAnswersStoredValue = window.localStorage.getItem(`gridAnswers_${currentGridId}`)
    gridAnswers = gridAnswersStoredValue ? JSON.parse(gridAnswersStoredValue) : [
        {}, {}, {},
        {}, {}, {},
        {}, {}, {}
    ]

    gridAnswers.forEach((gridAnswer, i) => {
        if (Object.keys(gridAnswer).length === 0) return
        const cell = document.getElementById(i + 1)

        const club = clubs.filter(c => c.id === gridAnswer.id)[0]

        fillCell(cell, club.shortName, club.logo, gridAnswer.score)
    })

    let allGuessesStoredValue = window.localStorage.getItem(`allGuesses_${currentGridId}`)
    allGuesses = allGuessesStoredValue ? JSON.parse(allGuessesStoredValue) : []

    document.getElementById("guesses").innerHTML = GUESSES_NUMBER - allGuesses.length

    document.getElementById("score").innerHTML = Math.round(gridScore * 100) / 100 // 2 decimal places

    if (gridIsComplete()) {
        showViewResultsButton()
        lockGrid()
    }

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

    grids.forEach(grid => {
        const gridOptionContainer = document.createElement('div')
        gridOptionContainer.className = 'dropdown-option'

        const gridName = document.createElement('span')
        gridName.textContent = `Grid #${grid.id} (${grid.starting_date})`

        const selectGridButton = document.createElement('button')

        selectGridButton.textContent = 'Play!'
        selectGridButton.classList.add('primary')
        selectGridButton.onclick = () => {
            location.replace(`/grid/${grid.id}`)
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

    let existingFinalModal = document.querySelector('.final-modal')

    if (existingFinalModal) {
        let shareButtonElement = document.getElementById("share")
        shareButtonElement.textContent = "📢 Share"
        shareButtonElement.classList.add('secondary')

        modalOverlay.style.display = 'flex'
        existingFinalModal.style.display = 'block'
        modalOverlay.onclick = exitFinalMode
    } else {

        modalOverlay.style.display = 'flex'

        const {
            solutions,
            row_conditions_descriptions,
            col_conditions_descriptions
        } = await getGridSolution(currentGridId)

        let finalModal = document.createElement("div")

        makeSolutionsGrid(finalModal, solutions, row_conditions_descriptions, col_conditions_descriptions, currentGridId)

        finalModal.classList.add("final-modal")

        modalOverlay.appendChild(finalModal)
        modalOverlay.onclick = exitFinalMode
    }
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
        showViewResultsButton()
    }
    lockGrid()
}

function showViewResultsButton() {
    const viewResultsButton = document.querySelector('.view-results')
    viewResultsButton.style.display = 'block'
    viewResultsButton.onclick = () => showFinalModal()
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

    let selectedCell = document.querySelector('.selected')

    const filteredClubs = clubs.filter(club => club.name.toLowerCase().includes(searchString));

    filteredClubs.forEach(club => {
        const optionContainer = document.createElement('div')
        optionContainer.className = 'dropdown-option'

        const clubName = document.createElement('span')
        clubName.textContent = club.name;

        const selectButton = document.createElement('button')
        if (gridAnswers.some(c => c.id === club.id) || allGuesses.some(c => c.id === club.id && c.cell === selectedCell.id)) {
            optionContainer.classList.add('disabled')
            selectButton.disabled = true
        }
        selectButton.textContent = 'Select'
        selectButton.classList.add('primary')
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

    let selectedCell = document.querySelector('.selected')
    fetch(url, {
        method: "POST", headers: {
            'Accept': 'application/json', "Content-Type": "application/json"
        }, body: JSON.stringify({
            "grid-id": currentGridId,
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
                let rarityScore = Math.floor(100 * data.total_club_answered / data.total_answers)

                fillCell(selectedCell, data.clubShortName, data.logo, rarityScore)

                let cellScore = isNaN(rarityScore) ? 0 : rarityScore

                gridScore += ((125 - cellScore) / 1125) * 100
                window.localStorage.setItem(`gridScore_${currentGridId}`, gridScore)
                document.getElementById("score").innerHTML = Math.round(gridScore * 100) / 100 // 2 decimal places

                gridAnswers[selectedCell.id - 1] = {"id": clubId, "score": cellScore}
                window.localStorage.setItem(`gridAnswers_${currentGridId}`, JSON.stringify(gridAnswers))
            } else {
                applyPowEffect(selectedCell)
                selectedCell.animate(
                    [{backgroundColor: 'darkred', offset: 0.3}],
                    {duration: 1000, iterations: 1}
                );
            }

            hideModal()
            allGuesses.push({id: clubId, cell: selectedCell.id})

            window.localStorage.setItem(`allGuesses_${currentGridId}`, JSON.stringify(allGuesses))

            document.getElementById("guesses").innerHTML = GUESSES_NUMBER - allGuesses.length
            if (gridIsComplete()) {
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

