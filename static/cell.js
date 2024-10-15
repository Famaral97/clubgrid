const rarities = {
    amateur: { rarityClass: 'amateur', rarityName: 'Amateur'},
    semiPro: { rarityClass: 'semi-pro', rarityName: 'Semi Pro'},
    pro: { rarityClass: 'pro', rarityName: 'Pro'},
    legend: { rarityClass: 'legend', rarityName: 'Legend'},
    ballonDor: { rarityClass: 'ballon-dor', rarityName: "Ballon d'Or"}
}


function getRarity(rarityScore) {
    if (rarityScore > 50){
        return rarities.amateur
    } else if (rarityScore > 20) {
        return rarities.semiPro
    } else if (rarityScore > 10) {
        return rarities.pro
    } else if (rarityScore > 5) {
        return rarities.legend
    } else {
        return rarities.ballonDor
    }
}


function fillCell(selectedCell, clubName, clubLogo, rarityScore) {

    let rarity = getRarity(rarityScore)

    selectedCell.style.cursor = 'default'
    selectedCell.onclick = null
    selectedCell.classList.add('correct')
    selectedCell.classList.add(rarity.rarityClass)
    selectedCell.classList.remove("grid-cell-active")
    selectedCell.style.backgroundColor = 'white'

    const clubNameElement = document.createElement("div")
    clubNameElement.textContent = clubName;
    clubNameElement.classList.add('answer-club-details')
    clubNameElement.classList.add(rarity.rarityClass)
    selectedCell.appendChild(clubNameElement)

    const clubLogoElement = document.createElement("div")
    clubLogoElement.style.backgroundImage = `url(${clubLogo})`
    clubLogoElement.classList.add('answer-club-logo');
    selectedCell.appendChild(clubLogoElement)

    const rarityElement = document.createElement("div")
    rarityElement.textContent = `${rarity.rarityName} - ${rarityScore > 0 ? rarityScore : 0}%`
    rarityElement.classList.add('answer-club-details')
    rarityElement.classList.add(rarity.rarityClass)
    selectedCell.appendChild(rarityElement)
}
