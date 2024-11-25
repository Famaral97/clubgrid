function makeClubdex(answeredClubs) {
    let tabCategories = [
        {prefix: "EN", name: "England"},
        {prefix: "DE", name: "Germany"},
        {prefix: "PT", name: "Portugal"},
        {prefix: "ES", name: "Spain"},
        {prefix: "IT", name: "Italy"},
        {prefix: "FR", name: "France"}
    ]

    let modalContainer = document.createElement("div")

    let tabsContainer = generateTabs(tabCategories)
    modalContainer.appendChild(tabsContainer)

    let tabContentContainer = document.createElement("div")
    tabCategories.forEach(tabCategory => {
        const tabContent = generateTabContent(tabCategory, answeredClubs)
        tabContentContainer.appendChild(tabContent);
    })
    modalContainer.appendChild(tabContentContainer)

    modalContainer.classList.add("clubdex-modal")

    return modalContainer
}

function generateTabs(tabCategories) {
    let tabsContainer = document.createElement("div")
    tabsContainer.classList.add("tabs")

    tabCategories.forEach(((tabCategory, index) => {
        const tab = document.createElement("button");
        tab.classList.add("tab")
        tab.classList.add("accent")
        tab.textContent = tabCategory.name
        tab.onclick = () => {
            highlightTab(index)
            showTab(index)
        }
        tabsContainer.appendChild(tab);
    }))

    return tabsContainer
}

function generateTabContent(tabCategory, answeredClubs) {
    const tabContentContainer = document.createElement("div");
    tabContentContainer.classList.add("tab-content");
    tabContentContainer.id = tabCategory.prefix;

    const cardsContainer = document.createElement("div");
    cardsContainer.classList.add("card-container")

    let collectedClubs = 0
    const clubsInTab = Object.values(clubs).filter(c => c.id.startsWith(tabCategory.prefix))
    clubsInTab.forEach(club => {
        let clubCard = document.createElement("div");
        clubCard.classList.add("card")

        let clubWasAnswered = answeredClubs.has(club.id)

        collectedClubs = clubWasAnswered ? (collectedClubs + 1) : collectedClubs;
        clubCard.textContent = clubWasAnswered ? club.name : "??????"

        cardsContainer.appendChild(clubCard)
    })

    let completionContainer = document.createElement("h3")
    completionContainer.textContent = collectedClubs + "/" + clubsInTab.length

    tabContentContainer.appendChild(completionContainer)
    tabContentContainer.appendChild(cardsContainer)

    return tabContentContainer
}

function highlightTab(indexOfSelected) {
        const tabs = document.querySelectorAll('.tab');

        tabs.forEach((tab, i) => {
            if (i === indexOfSelected) tab.classList.add('active')
            else tab.classList.remove('active')
        });
}

function showTab(index) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach((content, i) => {
        content.style.display = i === index ? 'block' : 'none';
    });
}