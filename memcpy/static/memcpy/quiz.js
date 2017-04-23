


/* Global variables */
// Timer handler for setInterval() and clearInterval()
timerHandler = null;
// Time left in milliseconds
timeLeft = -1;
// Count down unit: 0.1 second (100 ms)
timeUnit = 100;

// Timer reference: https://www.w3schools.com/howto/howto_js_countdown.asp
function quizTimer() {
    var seconds = timeLeft / 1000;

    // Display the result in the element with id = "timer"
    $("#timer").html(seconds.toFixed(1));

    // Time is up
    if (seconds <= 0) {
        window.clearInterval(timerHandler);
        // Change to red color
        $("#timer").css("color", "red");
        // $("#timer").text("Time Up");
    }

    // Reduce time left at each function call
    timeLeft -= timeUnit;
}

// The initialization to be called on page load
function quizInit(book_id) {
    // Quiz mode: count down for 10 seconds (10,000 ms)
    timeLeft = 10000;
    // Start the timer immediately
    quizTimer();
    timerHandler = window.setInterval(quizTimer, timeUnit);
}

