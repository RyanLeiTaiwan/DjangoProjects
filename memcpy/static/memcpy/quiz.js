/** JavaScript code to control the entire quiz.
 *  book_id is the only input parameter from HTML.
 *  Events in the quiz will trigger corresponding functions.
 */

/*** Global variables ***/

// Timer handler for setInterval() and clearInterval()
timerHandler = null;
// Time left in milliseconds
timeLeft = -1;
// Count down unit: 0.1 second (100 ms)
timeUnit = 100;

// Entry_list for the whole quiz, obtained by AJAX at the beginning
entry_list = null;
// Entry index indicates the progress (starts from 0)
cur_entry_index = 0;

// To be more sincere, start initialization only when the document is "ready"
// https://learn.jquery.com/using-jquery-core/document-ready/
function quizLoad(book_id) {
    $(document).ready(function() {
        quizInit(book_id);
    });
}

// The initialization to be called on page load
function quizInit(book_id) {
    // Quiz mode: count down for 10 seconds (10,000 ms)
    timeLeft = 10000;
    // Start the timer immediately
    quizTimer();
    timerHandler = window.setInterval(quizTimer, timeUnit);
    // Display the first question on success
    get_quiz_entries(book_id);
}

// Timer reference: https://www.w3schools.com/howto/howto_js_countdown.asp
function quizTimer() {
    // Cache the jQuery selection for performance. Get PyCharm warning otherwise.
    var timer = $("#timer");
    var seconds = timeLeft / 1000;
    // Display the result in the element with id = "timer"
    timer.html(seconds.toFixed(1));
    // Time is up
    if (seconds <= 0) {
        window.clearInterval(timerHandler);
        // Change to red color
        timer.css("color", "red");
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

// Use entry_list and cur_entry_index to display question
function displayQuestion() {
    // Debug zone!
    var true_ans = entry_list[cur_entry_index]["answer"];
    $("#js-debug").html("True Answer: " + sanitize(true_ans));

    var quiz_length = entry_list.length;
    // Progress in the quiz
    $("#quiz-progress-text").html("Question " + (cur_entry_index + 1) + " of " + quiz_length);
    var progress_bar = $("#quiz-progress-bar");
    var progress = (cur_entry_index + 1) / quiz_length * 100;
    progress_bar.attr("aria-valuenow", progress);
    progress_bar.css("width", progress + "%");

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
    $("#quiz-candidate-" + correct_candidate).html(cur_entry.answer);

    // For each other answer candidate, assign one other non-repeating random entry
    for (cand = 1; cand <= 4; cand++) {
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
                    $("#quiz-candidate-" + cand).html(entry_list[wrong_entry_index].answer);
                }
            }
        }
        
    }
}

