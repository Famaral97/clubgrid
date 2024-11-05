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
            <p>
                The displayed % indicates the % of correct answers the in that cell was used as an answer. The lower the value, the better is the rarity score.
            </p>
    
            <h2>Available Clubs</h2>
            <p>Clubs that, in 2024, played in the top league level:</p>
            <ul>
                <li>󠁧󠁢󠁥󠁮󠁧󠁿🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League</li>
                <li>🇩🇪 Bundesliga</li>
                <li>🇵🇹 Liga Portugal</li>
                <li>🇪🇸 La Liga</li>
                <li>🇮🇹 Serie A</li>
                <li>🇫🇷 Ligue 1</li>
            </ul>
            
            <h2>Score</h2>
            <p>The lower club the %, the better the result. Each answer's score takes into consideration:</p>
            <ul>
                <li><strong>Rarity of the answer:</strong> how often the club has been used as an answer for those conditions.</li> 
                <li><strong>Difficulty of the conditions:</strong> how many wrong answers there are for the given conditions.</li> 
            </ul>
            <p>This will translate to a final grid score, where 0 is the minimum and 100 the best score.</p>
    
            <h2>Conditions info and sources</h2>
            <p>Unless specified otherwise, all conditions refer to the main male football team of the club.</p>
            
            <h3>Logos</h3>
            <ul>
                    <li><strong>Logo has animal:</strong> any intentional representation of an animal, or part of an animal, humans included.</li>
                    <li><strong>Logo has a football:</strong> any intentional representation of football, modern or antique.</li>
                    <li><strong>Logo has X colors:</strong> borders and different shades count as different colors.</li>
                    <li><strong>Based in a capital city:</strong> the city where the club is based on is the capital.</li>
                    <li><strong>Logo is circular:</strong> logos that are almost perfect circles (e.g. if they have a crown on top, they do NOT qualify).</li>
            </ul>
            
            <h3>League titles</h3>
            <p>First division titles won</p>
            <ul>
                <li>
                    🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League, from 1888 to 2024. 
                    <a href="https://www.statista.com/statistics/383696/premier-league-wins-by-team/" target="_blank" >Source</a>
               </li>
                <li>
                    🇩🇪 Bundesliga, from 1903 to 2024. 
                    <a href="https://www.statista.com/statistics/1387762/most-bundesliga-titles/" target="_blank" >Source</a>
                </li>
                <li>
                    🇵🇹 Liga Portugal, from 1934 to 2024. 
                    <a href="https://www.zerozero.pt/competicao/liga-portuguesa/3/vencedores" target="_blank" >Source</a>
                </li>
                <li>
                    🇪🇸 La Liga, from 1929 to 2024. 
                    <a href="https://www.statista.com/statistics/783239/la-liga-list-of-football-teams-that-won-the-league-in-spain/" target="_blank" >Source</a>
                </li>
                <li>
                    🇮🇹 Serie A, from 1897 to 2024. 
                    <a href="https://www.statista.com/statistics/611319/soccer-winner-clubs-serie-a-games-in-italy/" target="_blank" >Source</a>
                </li>
                <li>
                    🇫🇷 Ligue 1, from 1932 to 2024.
                    <a href="https://www.statista.com/statistics/1387743/ligue-1-most-titles/" target="_blank" >Source</a>
                </li>
            </ul>
    
            <h3>European titles</h3>
            <ul>
                <li>
                    UEFA Champions League/European Cup. 
                    <a href="https://en.wikipedia.org/wiki/List_of_European_Cup_and_UEFA_Champions_League_finals" target="_blank" >Source</a>
                </li>
                <li>
                    Europa League/UEFA Cup 
                    <a href="https://en.wikipedia.org/wiki/List_of_UEFA_Cup_and_Europa_League_finals" target="_blank" >Source</a>
                </li>
                <li>
                    UEFA Cup Winners' Cup/European Cup Winners' Cup 
                    <a href="https://en.wikipedia.org/wiki/List_of_UEFA_Cup_Winners%27_Cup_finals" target="_blank" >Source</a>
                </li>
            </ul>
            
            <h3>Domestic Cup titles</h3>
            <p>They are related to the main cup competition in each country. They do <strong>NOT</strong> include League Cups.</p>
            <ul>
                <li>
                    🏴󠁧󠁢󠁥󠁮󠁧󠁿 FA Cup, from 1871 to 2024.
                    <a href="https://en.wikipedia.org/wiki/List_of_FA_Cup_finals" target="_blank" >Source</a>
                </li>
                <li>
                    🇩🇪 DFB Pokal, from 1935 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/List_of_DFB-Pokal_finals" target="_blank" >Source</a>
                </li>
                <li>
                    🇵🇹 Taça Portugal, from 1939 to 2024. 
                    <a href="https://pt.wikipedia.org/wiki/Ta%C3%A7a_de_Portugal" target="_blank" >Source</a>
                </li>
                <li>
                    🇪🇸 Copa Del Rey, from 1903 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/List_of_Copa_del_Rey_finals" target="_blank" >Source</a>
                </li>
                <li>
                    🇮🇹 Coppa Italia, from 1922 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/List_of_Coppa_Italia_finals" target="_blank" >Source</a>
                </li>                
                <li>
                    🇫🇷 Coupe de France, from 1918 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/List_of_Coupe_de_France_finals" target="_blank" >Source</a>
                </li>
            </ul>
            
            <h3>Domestic Super Cup titles</h3>
            <p>They are related to each country's Super Cup, being usually contested between the winners of the domestic league and the domestic cup. When a single club has won both, it goes on to face the domestic league runner-up.</p>
            <ul>
                <li>
                    🏴󠁧󠁢󠁥󠁮󠁧󠁿 FA Community Shield, from 1908 to 2024.
                    <a href="https://en.wikipedia.org/wiki/List_of_FA_Community_Shield_matches" target="_blank" >Source</a>
                </li>
                <li>
                    🇩🇪 DFL Supercup, from 1987 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/DFL-Supercup" target="_blank" >Source</a>
                </li>
                <li>
                    🇵🇹 Supertaça Cândido de Oliveira, from 1979 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/Superta%C3%A7a_C%C3%A2ndido_de_Oliveira" target="_blank" >Source</a>
                </li>
                <li>
                    🇪🇸 Supercopa de España, from 1982 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/Supercopa_de_Espa%C3%B1a" target="_blank" >Source</a>
                </li>
                <li>
                    🇮🇹 Supercoppa Italiana, from 1988 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/Supercoppa_Italiana" target="_blank" >Source</a>
                </li>                
                <li>
                    🇫🇷 Trophée des Champions, from 1955 to 2024. 
                    <a href="https://en.wikipedia.org/wiki/Troph%C3%A9e_des_Champions" target="_blank" >Source</a>
                </li>
            </ul>
            
            <h3>Transfermarkt Data</h3>
            <p>The following conditions were designed with data obtained from <a href="https://www.transfermarkt.com/" target="_blank">Transfermarkt</a>:</p>
            <ul>
                <li>Club names</li>
                <li>Stadium capacities</li>
                <li>Squad size</li>
                <li>Squad average age</li>
                <li>Number of foreigners in squad</li>
                <li>% of foreigners in squad</li>
                <li>National team players</li>
                <li>Net transfer record</li>
            </ul>
            
            <h3>Founding year</h3>
            <p>Taken from the club's wikipedia page, it was considered the earliest date of a foundation. For example, if a club was re-founded because of bankruptcy, that date was not taken into account.</p>
            
            <h3>Instagram Followers</h3>
            <p>Taken directly from each club's official Instagram page, in November 2024.</p>
        </div>
    `

    modalContainer.classList.add("info-modal")

    return modalContainer
}