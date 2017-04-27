/** JavaScript code to control the entire quiz.
 *  book_id is the only input parameter from HTML.
 *  Events in the quiz will trigger corresponding functions.
 */

/*** Global variables ***/

// Timer handler needed for setInterval() and clearInterval()
timerHandler = null;
// Pause handler needed for setInterval() and clearInterval()
pauseHandler = null;
// Quiz mode: count down for 10 seconds (10,000 ms)
timeLimit = 10000;
// Time left in milliseconds
timeLeft = -1;
// Count down unit: 0.1 second (100 ms)
timeUnit = 100;
// Time to pause after each question
timePause = 2000;
// Entry_list for the whole quiz, obtained by AJAX at the beginning
entry_list = null;
// Entry index indicates the progress (starts from 0)
cur_entry_index = 0;

// Copied from homework
function sanitize(s) {
    // Be sure to replace ampersand first
    // Yu-Heng Lei: adding my other replacements to resemble Django's filters
    // {{ post.text| nbsp | linebreaksbr }}
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/ /g, '&nbsp;')
            .replace(/\r\n/g, '<br>')
            .replace(/\n/g, '<br>')
            .replace(/\+/g, '&plus;');
}

// To be more sincere, perform quiz initialization only when the document is "ready"
// https://learn.jquery.com/using-jquery-core/document-ready/
function quizLoad(book_id) {
    $(document).ready(function() {
        quizInit(book_id);
    });
}

// The initialization to be called on page load
function quizInit(book_id) {
    // Initialize popup dialog
    dialogInit();

    // Get quiz entries, display the first question, and register events on success
    get_quiz_entries(book_id);
    /** Cannot put AJAX on-success statements here here because the DB query is asynchronous **/
}

function dialogInit() {
    var popup = $("#quiz-dialog");
    popup.dialog({
        autoOpen: false,
        show: {
            effect: "fade",
            duration: 1000
        },
        hide: {
            effect: "fade",
            duration: 500
        }
    });

    // Debugging
    popup.text("jQuery UI Dialog debugging");
    popup.dialog("open");
}

// Timer reference: https://www.w3schools.com/howto/howto_js_countdown.asp
function quizTimer() {
    // Cache the jQuery selection for performance. Get PyCharm warning otherwise.
    var timer = $("#timer");
    var seconds = timeLeft / 1000;
    // Display the result in the element with id = "timer"
    timer.html(seconds.toFixed(1));
    // Time is up
    if (timeLeft <= 0) {
        window.clearInterval(timerHandler);
        timeLeft = 0;
        seconds = 0;
        timer.html(seconds.toFixed(1));
        // Change to red color
        timer.css("color", "red");
        // Simulate wrong answer by answering "candidate 0"
        handleAnswer(0);
    }
    // Reduce time left at each function call
    timeLeft -= timeUnit;
}

// Get at most 20 entries in a quiz
function get_quiz_entries(book_id) {
    // http://api.jquery.com/jQuery.ajax/#jqXHR
    $.ajax({
        url: "/memcpy/quiz-entries/" + book_id,
        type: "GET",
        dataType : "json",
        success: function(data) {
            // Save the response data to entry_list
            entry_list = data;
            displayQuestion();
        },
        error: function(jqXHR) {
            $("#json-error-text").text("AJAX error: " + jqXHR.responseText);
            // Make the JSON error box visible (it was hidden)
            $("#json-error-box").css("display", "block");
            console.log("AJAX error: " + jqXHR.responseText);
        }
    });
}

// Use entry_list and cur_entry_index to display question
function displayQuestion() {
    // Stop the pause timer
    window.clearInterval(pauseHandler);

    // Debug zone!
    var true_ans = entry_list[cur_entry_index]["answer"];
    $("#js-debug").html("True Answer: " + sanitize(true_ans));
    console.log("cur_entry_index: " + cur_entry_index);

    var quiz_length = entry_list.length;
    // Show quiz progress in text
    $("#quiz-progress-text").html("Question " + (cur_entry_index + 1) + " of " + quiz_length);

    // Current entry
    var cur_entry = entry_list[cur_entry_index];
    var entry_id = cur_entry.entry_id;
    var question_text = cur_entry.question_text;
    // JSON only contains a boolean value for question_image
    var question_image = cur_entry.question_image;
    if (question_text !== null) {
        $("#quiz-question-text").html(sanitize(question_text));
    }
    if (question_image !== false) {
        $("#quiz-question-image").html(
            "<div><img class='entry_table img-rounded' src='/memcpy/entry_photo/" + entry_id + "'></div>");
    }

    /* There is no built-in "random sample" function in JavaScript! Use the brute-force way */
    // Entry index in every answer candidate (index 0 is not used)
    var cand_entry_index = [-1, -1, -1, -1, -1];
    // Assign current entry to one random answer candidate (1-4)
    var correct_candidate = Math.floor((Math.random() * 4) + 1);
    cand_entry_index[correct_candidate] = cur_entry;
    $("#quiz-candidate-text-" + correct_candidate).html(cur_entry.answer);

    // For each other answer candidate, assign one other non-repeating random entry
    for (var cand = 1; cand <= 4; cand++) {
        // Skip the correct candidate
        if (cand !== correct_candidate) {
            var done = false;
            // Randomly sample one entry until done
            while (!done) {
                var wrong_entry_index = Math.floor(Math.random() * quiz_length);
                // Don't use correct or repeating entry
                if (wrong_entry_index !== cur_entry_index && cand_entry_index.indexOf(wrong_entry_index) === -1) {
                    cand_entry_index[cand] = wrong_entry_index;
                    done = true;
                    $("#quiz-candidate-text-" + cand).html(entry_list[wrong_entry_index].answer);
                }
            }
        }
    }

    // Register for click, keypress, and time-out events
    registerEvents();
    // Reset and start the timer
    timeLeft = timeLimit;
    window.clearInterval(timerHandler);
    timerHandler = window.setInterval(quizTimer, timeUnit);
}

function registerEvents() {
    for (var cand = 1; cand <= 4; cand++) {
        // Call handleAnswer on button clicks
        var cand_button = $("#quiz-candidate-btn-" + cand);
        // Fix "Mutable variable is accessible from closure" bug. Otherwise, the answer is 5!
        // http://stackoverflow.com/questions/6288571/creating-jquery-click-functions-with-for-loop
        // http://stackoverflow.com/questions/4091765/assign-click-handlers-in-for-loop
        (function (ans) {
            cand_button.click(function () {
                handleAnswer(ans);
            });
        })(cand);
    }

    // Call handleAnswer on keypress (1-4)
    $(document).keypress(function (event) {
        var key = event.which || event.keyCode;
        // Keycodes for (0, 1, 2, 3, 4) are (48, 49, 50, 51, 52)
        if (key >= 49 && key <= 52) {
            handleAnswer(key - 48);
        }
    });
}

function unregisterEvents() {
    for (var cand = 1; cand <= 4; cand++) {
        var cand_button = $("#quiz-candidate-btn-" + cand);
        cand_button.off("click");
    }
    $(document).off("keypress");
}

// Pause Javascript execution
// http://stackoverflow.com/questions/16623852/how-to-pause-javascript-code-excution-for-2-seconds
function sleep(miliseconds) {
   var currentTime = new Date().getTime();
   while (currentTime + miliseconds >= new Date().getTime()) {
   }
}

// Handle answers on click, keypress, or time-up. However, this is NOT a standard Javascript event handler
function handleAnswer(candidate) {
    var quiz_length = entry_list.length;
    console.log("You answered " + candidate);
    // Stop the timer
    window.clearInterval(timerHandler);
    // Unregister all event listeners to prevent the user from repeated answering
    unregisterEvents();

    // Pause for a moment before moving on to the next question
    pauseHandler = window.setInterval(function() {
        cur_entry_index++;
        // Move the progress bar
        var progress_bar = $("#quiz-progress-bar");
        var progress = cur_entry_index / quiz_length * 100;
        progress_bar.attr("aria-valuenow", progress);
        progress_bar.css("width", progress + "%");

        if (cur_entry_index === quiz_length) {
            // Quiz is finished
            window.clearInterval(pauseHandler);
            timeLeft = timeLimit;
            // TODO: Display quiz result in a jQuery UI popup Dialog
            var popup = $("#quiz-dialog");
            popup.text("This is your quiz result");
            popup.dialog("open");
        } else {
            // Quiz is not finished
            $("#timer").css("color", "black");
            displayQuestion();
        }
    }, timePause);
}
