document.addEventListener('DOMContentLoaded', function () {

    var countdownDuration = 3600;
    var element = document.querySelector('#timer');
    startCountdown(countdownDuration, element);

});

function startCountdown(duration, display) {
    var timer = duration;
    var minutes;
    var seconds;
    
    setInterval(function () {
      minutes = parseInt(timer / 60, 10);
      seconds = parseInt(timer % 60, 10);
  
      if (minutes < 10) {
        minutes = "0" + minutes;
      }

      if (seconds < 10) {
        seconds = "0" + seconds;
      }
  
      display.textContent = minutes + ":" + seconds;
  
      timer = timer - 1;
      if (timer < 0) {
        timer = duration;
      }
    }, 1000);
  }