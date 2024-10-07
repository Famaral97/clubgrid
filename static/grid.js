let all_solutions = []

function makeGrid(container, solutions, row_conditions_descriptions, col_conditions_descriptions) {

    all_solutions = solutions

    container.innerHTML = `
    <h1>Solutions</h1>
    <p>Click on a cell to check all possible clubs</p>
    <div class="container-solutions">
        <!-- Top-left corner is empty for the grid layout -->
        <div class="empty-cell"></div>
        <div class="condition">${col_conditions_descriptions[0]}</div>
        <div class="condition">${col_conditions_descriptions[1]}</div>
        <div class="condition">${col_conditions_descriptions[2]}</div>

        <!-- Row 1 -->
        <div class="condition">${row_conditions_descriptions[0]}</div>
        <div onclick="showSolutionModal(0,0)" class="grid-cell">${solutions[0][0].clubs.length} answers</div>
        <div onclick="showSolutionModal(0,1)" class="grid-cell">${solutions[0][1].clubs.length} answers</div>
        <div onclick="showSolutionModal(0,2)" class="grid-cell">${solutions[0][2].clubs.length} answers</div>

        <!-- Row 2 -->
        <div class="condition">${row_conditions_descriptions[1]}</div>
        <div onclick="showSolutionModal(1,0)" class="grid-cell">${solutions[1][0].clubs.length} answers</div>
        <div onclick="showSolutionModal(1,1)" class="grid-cell">${solutions[1][1].clubs.length} answers</div>
        <div onclick="showSolutionModal(1,2)" class="grid-cell">${solutions[1][2].clubs.length} answers</div>
        <!-- Row 3 -->
        <div class="condition">${row_conditions_descriptions[2]}</div>
        <div onclick="showSolutionModal(2,0)" class="grid-cell">${solutions[2][0].clubs.length} answers</div>
        <div onclick="showSolutionModal(2,1)" class="grid-cell">${solutions[2][1].clubs.length} answers</div>
        <div onclick="showSolutionModal(2,2)" class="grid-cell">${solutions[2][2].clubs.length} answers</div>
    </div>
    `
}

function showSolutionModal(row, col) {
    const {clubs, total_guesses} = all_solutions[row][col]

    extraModelOverlay.style.display = 'flex'

    let solutionsModal = document.createElement("div")
    solutionsModal.classList.add("solutions-modal")

    clubs.forEach((club) => {
        const solutionContainer = document.createElement("div")
        solutionContainer.classList.add("dropdown-option")
        solutionContainer.style.height = '110px'

        const clubName = document.createElement("div")
        clubName.innerHTML = `
            <h3>${club.name}</h3>
            <p>Total guesses: ${club.answer_count} (${Math.floor(100*club.answer_count/total_guesses)}%)</p>
        `
        solutionContainer.appendChild(clubName)

        const clubLogo = document.createElement("div")
        clubLogo.classList.add("solutions-club-logo")
        clubLogo.style.backgroundImage = `url(${club.logo})`
        solutionContainer.appendChild(clubLogo)

        solutionsModal.appendChild(solutionContainer)
    })

    extraModelOverlay.appendChild(solutionsModal)
}

