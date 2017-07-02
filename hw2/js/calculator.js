// Internal vairables
var new_val, prev_val, prev_op, prev_click;

function reset() {
    new_val = 0;
    prev_val = 0;
    // Initial operator: "=" 
    prev_op = "=";
    prev_click = "";
    document.getElementById('result').value = new_val;
    console.log("reset()");
}

function clickDigit(digit) {
    // Inserting a decimal number from the right
    new_val = new_val * 10 + digit;
    console.log("new_val: " + new_val);
    document.getElementById('result').value = new_val;
    prev_click = digit;
}

function clickOperator(new_op) {
    // Check for consecutive operators: only update the operator
    if (prev_click == "+" || prev_click == "-" || prev_click == "*" || prev_click == "/") {
        prev_op = new_op;
        prev_click = new_op;
        console.log("prev_op & prev_click: " + prev_op + ", " + prev_click);
        return;
    }

    // Compute the result
    var result = 0;
    switch (prev_op) {
        // Also the initial case
        case "=":
            result = new_val;
            break;
        case "+":
            result = prev_val + new_val;
            break;
        case "-":
            result = prev_val - new_val;
            break;
        case "*":
            result = prev_val * new_val;
            break;
        case "/":
            // Detect division by zero
            if (new_val == 0) {
                alert('Division by zero!');
                reset();
                return;
            }
            // Integer division
            result = Math.floor(prev_val / new_val);
            break;
    }
    console.log("result: " + result);
    document.getElementById('result').value = result;

    // Update variables
    prev_val = result;
    prev_op = new_op;
    new_val = 0;
    prev_click = new_op;
    console.log("prev_val: " + prev_val + ", prev_op: " + prev_op + ", new_val: " + new_val);
}

// Map keypress/keydown events to click events for easier testing
function keyPress(event) {
    // http://www.w3schools.com/jsref/event_key_keycode.asp
    var key = event.which || event.keyCode;
    // Digits
    if (key >= 48 && key <= 57) {
        clickDigit(key - 48);
        return;
    }
    // Reset: C or c
    if (key == 67 || key == 99) {
        reset();
        return;
    }
    // "+"
    if (key == 43) {
        clickOperator("+");
        return;
    }
    // "-"
    if (key == 45) {
        clickOperator("-");
        return;
    }
    // "*"
    if (key == 42) {
        clickOperator("*");
        return;
    }
    // "/"
    if (key == 47) {
        clickOperator("/");
        return;
    }
    // "=" or Enter
    if (key == 61 || key == 13) {
        clickOperator("=");
        return;
    }
}

function keyDown(event) {
    var key = event.which || event.keyCode;
    // Reset: ESC
    if (key == 27) {
        reset();
        return;
    }
}

