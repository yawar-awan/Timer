const startButton = document.getElementById("start-button");
const timeInput = document.getElementById("input-time");

let countdownInterval;

function startCountdown() {
  clearInterval(countdownInterval);
  const countDownTime = new Date().getTime() + getTimeInMilliseconds(timeInput.value);
  countdownInterval = setInterval(function() {
    const now = new Date().getTime();
    const distance = countDownTime - now;
    if (distance < 0) {
      clearInterval(countdownInterval);
      playSound();
      window.alert("Time is up!");
    } else {
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
      document.getElementById("countdown-timer").innerHTML = `${hours}h : ${minutes}m : ${seconds}s`;
    }
  }, 1000);
}

function getTimeInMilliseconds(timeString) {
  const [hours, minutes, seconds] = timeString.split(":");
  return (parseInt(hours) * 60 * 60 + parseInt(minutes) * 60 + parseInt(seconds)) * 1000;
}

function playSound() {
  const audio = new Audio("sound.mp3");
  audio.play();
}

startButton.addEventListener("click", startCountdown);
