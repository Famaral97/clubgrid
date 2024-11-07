async function getData() {
    const url = "/clubs";
    await fetch(url) // Replace with the actual API URL
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch clubs');
            }
            return response.json()
        })
        .then(data => {
            clubs = data
        })
        .catch(error => {
            console.error('Error fetching clubs:', error)
            window.location.reload()
        });
}

async function getGrids() {
    fetch("/grids").then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch grids');
        }
        return response.json()
    })
        .then(data => {
            grids = data
        })
        .catch(error => {
            console.error('Error fetching grids:', error)
            window.location.reload()
        });
}

async function getGridSolution(gridId) {
    return fetch(`/grid/${gridId}/end`).then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch grids');
        }
        return response.json()
    })
        .then(data => {
            return data
        })
        .catch(error => {
            console.error('Error fetching solutions:', error)
            window.location.reload()
        });
}