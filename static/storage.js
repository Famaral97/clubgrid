const STORAGE_VERSION = "v0.1"

const GRID_SCORE_LS = "gridScore"
const GRID_ANSWERS_LS = "gridAnswers"
const ALL_GUESSES_LS = "allGuesses"

function manageLocalStorage() {
    // Code to migrate older versions to new ones

    deleteDeprecatedLocalStorage()
}

function deleteDeprecatedLocalStorage() {
    for (let i = 0; i < localStorage.length; i++) {
        let item = localStorage.key(i)
        if (!item.startsWith(STORAGE_VERSION)) {
            localStorage.removeItem(item);
        }
    }
}

function getStoredGridScore(gridId) {
    return parseFloat(window.localStorage.getItem(`${STORAGE_VERSION}_${GRID_SCORE_LS}_${gridId}`))
}

function storeGridScore(gridId, score) {
    window.localStorage.setItem(`${STORAGE_VERSION}_${GRID_SCORE_LS}_${gridId}`, score)
}

function getStoredGridAnswers(gridId) {
    return window.localStorage.getItem(`${STORAGE_VERSION}_${GRID_ANSWERS_LS}_${gridId}`)
}

function storeGridAnswers(gridId, gridAnswers) {
    window.localStorage.setItem(`${STORAGE_VERSION}_${GRID_ANSWERS_LS}_${gridId}`, JSON.stringify(gridAnswers))
}

function getStoredAllGuesses(gridId) {
    return window.localStorage.getItem(`${STORAGE_VERSION}_${ALL_GUESSES_LS}_${gridId}`)
}

function storeAllGuesses(gridId, allGuesses) {
    window.localStorage.setItem(`${STORAGE_VERSION}_${ALL_GUESSES_LS}_${gridId}`, JSON.stringify(allGuesses))
}