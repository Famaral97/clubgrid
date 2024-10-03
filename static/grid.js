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
        <div onclick="showSolutionModal(0,0)" class="grid-cell">${solutions[0][0].length} answers</div>
        <div onclick="showSolutionModal(0,1)" class="grid-cell">${solutions[0][1].length} answers</div>
        <div onclick="showSolutionModal(0,2)" class="grid-cell">${solutions[0][2].length} answers</div>

        <!-- Row 2 -->
        <div class="condition">${row_conditions_descriptions[1]}</div>
        <div onclick="showSolutionModal(1,0)" class="grid-cell">${solutions[1][0].length} answers</div>
        <div onclick="showSolutionModal(1,1)" class="grid-cell">${solutions[1][1].length} answers</div>
        <div onclick="showSolutionModal(1,2)" class="grid-cell">${solutions[1][2].length} answers</div>
        <!-- Row 3 -->
        <div class="condition">${row_conditions_descriptions[2]}</div>
        <div onclick="showSolutionModal(2,0)" class="grid-cell">${solutions[2][0].length} answers</div>
        <div onclick="showSolutionModal(2,1)" class="grid-cell">${solutions[2][1].length} answers</div>
        <div onclick="showSolutionModal(2,2)" class="grid-cell">${solutions[2][2].length} answers</div>
    </div>
    `
}

function showSolutionModal(row, col) {
    const solutions = all_solutions[row][col]
    extraModelOverlay.style.display = 'flex'

    let solutionsModal = document.createElement("div")
    solutionsModal.classList.add("solutions-modal")

    solutions.forEach((solution) => {
        const solutionContainer = document.createElement("div")
        solutionContainer.classList.add("dropdown-option")
        solutionContainer.style.height = '110px'

        const clubName = document.createElement("div")
        clubName.innerHTML = solution.name
        solutionContainer.appendChild(clubName)

        const clubLogo = document.createElement("div")
        clubLogo.style.width = '100px'
        clubLogo.style.height = '100px'
        clubLogo.style.backgroundSize = 'contain'
        clubLogo.style.backgroundRepeat = 'no-repeat'
        clubLogo.style.backgroundPosition = 'center'
        clubLogo.style.backgroundImage = `url(${solution.logo})`
        solutionContainer.appendChild(clubLogo)

        solutionsModal.appendChild(solutionContainer)
    })

    extraModelOverlay.appendChild(solutionsModal)
}

