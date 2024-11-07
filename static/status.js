function checkServerStatus() {
  fetch(window.location.href, { method: 'GET', cache: 'no-store' })
    .then(response => {
      if (response.status === 500) {
        console.log("Internal Server Error detected. Attempting to reload...");
        // Reload the page after a short delay
        setTimeout(() => {
          window.location.reload()
        }, 1000); // 3-second delay (adjust if needed)
      }
    })
    .catch(error => {
        console.error("Error checking server status:", error)
        window.location.reload()
    });
}