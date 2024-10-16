let all_solutions = []

function makeSolutionsGrid(container, solutions, row_conditions_descriptions, col_conditions_descriptions, gridId) {
    all_solutions = solutions

    let resultAsText = getGridResultText()

    container.innerHTML = `
    <div>
        <h1>Results</h1>
        <div>
            <span style="white-space: pre-line; font-size: x-large">${resultAsText}</span>
            <span>Score: ${Math.round(gridScore * 100) / 100}</span>
            <br>
            <span>Guesses left: ${GUESSES_NUMBER - allGuesses.length}</span>
        </div>
        <br>
        <button id="share" onclick="copyResultToClipboard(`+gridId+`)">📢 Share</button>
        
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
            <div onclick="showSolutionModal(0,0)" class="grid-cell grid-cell-active">${solutions[0][0].clubs.length} answers</div>
            <div onclick="showSolutionModal(0,1)" class="grid-cell grid-cell-active">${solutions[0][1].clubs.length} answers</div>
            <div onclick="showSolutionModal(0,2)" class="grid-cell grid-cell-active">${solutions[0][2].clubs.length} answers</div>
    
            <!-- Row 2 -->
            <div class="condition">${row_conditions_descriptions[1]}</div>
            <div onclick="showSolutionModal(1,0)" class="grid-cell grid-cell-active">${solutions[1][0].clubs.length} answers</div>
            <div onclick="showSolutionModal(1,1)" class="grid-cell grid-cell-active">${solutions[1][1].clubs.length} answers</div>
            <div onclick="showSolutionModal(1,2)" class="grid-cell grid-cell-active">${solutions[1][2].clubs.length} answers</div>
            
            <!-- Row 3 -->
            <div class="condition">${row_conditions_descriptions[2]}</div>
            <div onclick="showSolutionModal(2,0)" class="grid-cell grid-cell-active">${solutions[2][0].clubs.length} answers</div>
            <div onclick="showSolutionModal(2,1)" class="grid-cell grid-cell-active">${solutions[2][1].clubs.length} answers</div>
            <div onclick="showSolutionModal(2,2)" class="grid-cell grid-cell-active">${solutions[2][2].clubs.length} answers</div>
        </div>
    </div>
    `
}

function showSolutionModal(row, col) {
    const {clubs, total_correct_answers} = all_solutions[row][col]

    extraModalOverlay.style.display = 'flex'

    let solutionsModal = document.createElement("div")
    solutionsModal.classList.add("solutions-modal")

    clubs.forEach((club) => {
        const solutionContainer = document.createElement("div")
        solutionContainer.classList.add("dropdown-option")
        solutionContainer.style.height = '110px'

        const clubName = document.createElement("div")
        let rarity_score = Math.floor(100 * club.total_club_answered / total_correct_answers)
        clubName.innerHTML = `
            <h3>${club.name}</h3>
            <p>Total guesses: ${club.total_club_answered} (${rarity_score > 0 ? rarity_score : 0}%)</p>
        `
        solutionContainer.appendChild(clubName)

        const clubLogo = document.createElement("div")
        clubLogo.classList.add("solutions-club-logo")
        clubLogo.style.backgroundImage = `url(${club.logo})`
        solutionContainer.appendChild(clubLogo)

        solutionsModal.appendChild(solutionContainer)
    })

    extraModalOverlay.appendChild(solutionsModal)
}

function copyResultToClipboard(gridId) {
    let sharedResult = `Club Grid #${gridId}\n`

    sharedResult += getGridResultText()

    sharedResult += `\nScore: ${Math.round(gridScore * 100) / 100}`

    sharedResult += `\nGuesses left: ${GUESSES_NUMBER - allGuesses.length}`

    sharedResult += `\nhttps://clubgrid.pythonanywhere.com/grid/${gridId}`

    navigator.clipboard.writeText(sharedResult);

    let shareButtonElement = document.getElementById("share");
    shareButtonElement.textContent = "Copied to clipboard!";
}

function getGridResultText() {
    let resultAsText = ""

    gridAnswers.forEach(((answer, i) => {
        if (Object.keys(answer).length !== 0) {
            if (answer.score > 50){
                resultAsText += "⚪"
            } else if (answer.score > 20) {
                resultAsText += "🟢"
            } else if (answer.score > 10) {
                resultAsText += "🔵"
            } else if (answer.score > 5) {
                resultAsText += "🟣"
            } else {
                resultAsText += "🟡"
            }
        }
        else resultAsText += "❌"
        if ((i+1) % 3 === 0) resultAsText += "\n"
    }))

    return resultAsText
}

function lockGrid() {
    document.querySelectorAll('.container .grid-cell').forEach(cell => {
        cell.onclick = null
        cell.classList.remove("grid-cell-active")
    })
}

function gridIsComplete() {
    return gridAnswers.filter(c => Object.keys(c).length !== 0).length === 9 || allGuesses.length === GUESSES_NUMBER
}
