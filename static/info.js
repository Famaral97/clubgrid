function displayInfo() {
    let modalContainer = document.createElement("div")

    modalContainer.innerHTML = `
        <div>
            <h1>Welcome to Club Grid</h1>
            <p>
                The place where you can put your football club knowledge to the test!
            </p>
            <p>
                Click on a grid space and find a club which respects the conditions written in the respective column and
                row.
            </p>
    
            <h2>Available Clubs</h2>
            <p>Clubs that, in 2024, played in:</p>
            <ul>
                <li>Portuguese Liga Portugal</li>
                <li>Spanish La Liga</li>
                <li>German Bundesliga</li>
                <li>English Premier League</li>
                <li>French Ligue 1</li>
                <li>Italian Serie A</li>
            </ul>
    
            <h2>Conditions info and sources</h2>
    
            <h3>League titles</h3>
            <p>First division titles won</p>
            <ul>
                <li>German Bundesliga, from 1903 to 2024. <a
                        href="https://www.statista.com/statistics/1387762/most-bundesliga-titles/">Source</a></li>
                <li>Italian Serie A, from 1897 to 2024. <a
                        href="https://www.statista.com/statistics/611319/soccer-winner-clubs-serie-a-games-in-italy/">Source</a>
                </li>
                <li>Spanish La Liga, from 1929 to 2024. <a
                        href="https://www.statista.com/statistics/783239/la-liga-list-of-football-teams-that-won-the-league-in-spain/">Source</a>
                </li>
                <li>French Ligue 1, from 1932 to 2024. <a
                        href="https://www.statista.com/statistics/1387743/ligue-1-most-titles/">Source</a></li>
                <li>Portuguese Liga Portugal, from 1934 to 2024. <a
                        href="https://www.zerozero.pt/competicao/liga-portuguesa/3/vencedores">Source</a></li>
                <li>English Premier League, from 1888 to 2024. <a
                        href="https://www.statista.com/statistics/383696/premier-league-wins-by-team/">Source</a></li>
            </ul>
    
            <h3>European titles</h3>
            <p>First division titles won</p>
            <ul>
                <li>UEFA Champions League/European Cup. <a
                        href="https://en.wikipedia.org/wiki/List_of_European_Cup_and_UEFA_Champions_League_finals">Source</a>
                </li>
                <li>Europa League/UEFA Cup <a
                        href="https://en.wikipedia.org/wiki/List_of_UEFA_Cup_and_Europa_League_finals">Source</a></li>
            </ul>
        </div>
    `

    modalContainer.classList.add("info-modal")

    return modalContainer
}