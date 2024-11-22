function makeCollection(answeredClubs) {
    let countryCodes = ["PT", "EN", "ES", "DE", "IT", "FR"]

    let modalContainer = document.createElement("div")

    let tabsContainer = generateTabs(countryCodes)
    modalContainer.appendChild(tabsContainer)

    let cardsContainer = document.createElement("div")
    countryCodes.forEach(countryCode => {
        const cards = generateCards(countryCode, answeredClubs)
        cardsContainer.appendChild(cards);
    })
    modalContainer.appendChild(cardsContainer)

    modalContainer.classList.add("info-modal")

    return modalContainer
}

function generateTabs(countryCodes) {
    let tabsContainer = document.createElement("div")
    tabsContainer.classList.add("tabs")

    countryCodes.forEach(((countryCode, index) => {
        const tab = document.createElement("button");
        tab.classList.add("tab")
        tab.classList.add("accent")
        tab.textContent = countryCode
        tab.onclick = () => {
            showTab(index)
        }
        tabsContainer.appendChild(tab);
    }))

    return tabsContainer
}

function generateCards(countryCode, answeredClubs) {
    const tabContentDiv = document.createElement("div");
    tabContentDiv.classList.add("tab-content");
    tabContentDiv.id = countryCode;

    const tabCardContainer = document.createElement("div");
    tabCardContainer.classList.add("card-container")

    const clubsInTab = Object.values(clubs).filter(c => c.id.startsWith(countryCode))
    clubsInTab.forEach(club => {
        let clubCard = document.createElement("div");
        clubCard.classList.add("card")
        clubCard.textContent = answeredClubs.has(club.id) ? club.name : "??????"

        tabCardContainer.appendChild(clubCard)
    })

    tabContentDiv.appendChild(tabCardContainer)

    return tabContentDiv
}

function showTab(index) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach((content, i) => {
        content.style.display = i === index ? 'block' : 'none';
    });
}