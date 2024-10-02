let all_solutions = []

function makeGrid(container, solutions, row_conditions_descriptions, col_conditions_descriptions) {

    all_solutions = solutions



    container.innerHTML = `
    <div class="container">
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
    console.log(all_solutions[row][col])
}