function fillCell(selectedCell, clubName, clubLogo, rarityScore) {
    selectedCell.style.cursor = 'default'
    selectedCell.onclick = null
    selectedCell.classList.add('correct')
    selectedCell.classList.remove("grid-cell-active")

    const clubNameElement = document.createElement("div")
    clubNameElement.textContent = clubName;
    clubNameElement.classList.add('answer-club-details')
    selectedCell.appendChild(clubNameElement)

    const clubLogoElement = document.createElement("div")
    clubLogoElement.style.backgroundImage = `url(${clubLogo})`
    clubLogoElement.classList.add('answer-club-logo');
    selectedCell.appendChild(clubLogoElement)

    const rarityElement = document.createElement("div")
    rarityElement.textContent = `${rarityScore > 0 ? rarityScore : 0}%`
    rarityElement.classList.add('answer-club-details')
    selectedCell.appendChild(rarityElement)
}
