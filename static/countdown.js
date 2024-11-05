function startCountdownToMidnight() {
  const countdownElement = document.getElementById("countdown");

  function updateCountdown() {
    const now = new Date();

    const midnightGMT = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1, 0, 0, 0));

    const timeLeft = midnightGMT - now;

    const hours = Math.floor((timeLeft / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((timeLeft / (1000 * 60)) % 60);
    const seconds = Math.floor((timeLeft / 1000) % 60);

    const hoursDisplay = hours < 10 ? "0" + hours : hours;
    const minutesDisplay = minutes < 10 ? "0" + minutes : minutes;
    const secondsDisplay = seconds < 10 ? "0" + seconds : seconds;

    countdownElement.textContent = `${hoursDisplay}:${minutesDisplay}:${secondsDisplay}`
  }

  updateCountdown();

  setInterval(updateCountdown, 1000);
}