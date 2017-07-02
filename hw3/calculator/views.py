from django.shortcuts import render


def reset(request):
    cxt = {}
    resetContext(cxt)
    # print('cxt: ' + str(cxt))
    return render(request, 'calculator/calculator.html', cxt)


# Reset context, but don't render the page
def resetContext(cxt, error=''):
    cxt['new_val'] = 0
    cxt['prev_val'] = 0
    # Initial operator: "="
    cxt['prev_op'] = 'equals'
    cxt['result'] = 0
    cxt['prev_click'] = ''
    cxt['error'] = error
    print('reset()')


# Receive hidden POST data and put in context
# Return an error string on validation error
def postToContext(post):
    cxt = {}
    op_list = ['plus', 'minus', 'times', 'divide', 'equals']
    digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    click_list = [''] + digit_list + op_list

    # Validation: missing names, integer conversions, operator strings
    if 'new_val' not in post:
        return 'Missing new_val data'
    # new_val: all-digit integers (excluding +0, -0)
    if post['new_val'].isdigit():
        cxt['new_val'] = int(post['new_val'])
    else:
        return 'Invalid new_val value'

    if 'prev_val' not in post:
        return 'Missing prev_val data'
    # prev_val: positive/negative integers
    try:
        cxt['prev_val'] = int(post['prev_val'])
    except ValueError:
        return 'Invalid prev_val value'

    if 'prev_op' not in post:
        return 'Missing prev_op data'
    prev_op = post['prev_op']
    if prev_op in op_list:
        cxt['prev_op'] = post['prev_op']
    else:
        return 'Invalid prev_op value'

    if 'result' not in post:
        return 'Missing result data'
    # result: positive-negative integers
    try:
        cxt['result'] = int(post['result'])
    except ValueError:
        return 'Invalid result value'

    if 'prev_click' not in post:
        return 'Missing prev_click data'
    prev_click = post['prev_click']
    if prev_click in click_list:
        cxt['prev_click'] = post['prev_click']
    else:
        return 'Invalid prev_click value'

    if 'error' not in post:
        return 'Missing error data'
    return cxt


def click(request):
    post = request.POST
    print('POST data: ' + str(post))
    cxt = postToContext(post)
    print('cxt: ' + str(cxt))
    # Validation result of postToContext()
    if type(cxt) == str:
        err = cxt
        cxt = {}
        resetContext(cxt, err)
        return render(request, 'calculator/calculator.html', cxt)

    if 'btn_reset' in post:
        resetContext(cxt)
    elif 'btn_digit' in post:
        # Validation: only accept single character [0-9]
        digit_str = post['btn_digit']
        if digit_str.isdigit() and len(digit_str) == 1:
            digit = int(digit_str)
            clickDigit(digit, cxt)
        else:
            print('Invalid [0-9] digit')
            resetContext(cxt, 'Invalid [0-9] digit')
    elif 'btn_op' in post:
        # Validation: only accept "+-*/=" operators
        op_list = ['plus', 'minus', 'times', 'divide', 'equals']
        op = post['btn_op']
        if op in op_list:
            clickOperator(op, cxt, request)
        else:
            print('Invalid [+-*/=] operator')
            resetContext(cxt, 'Invalid [+-*/=] operator')
    else:
        print('Invalid <button> name')
        resetContext(cxt, 'Invalid <button> name')
    return render(request, 'calculator/calculator.html', cxt)


def clickDigit(digit, cxt):
    # Inserting a decimal number from the right
    cxt['new_val'] = cxt['new_val'] * 10 + digit
    cxt['result'] = cxt['new_val']
    cxt['prev_click'] = digit
    print('new_val & result: ' + str(cxt['new_val']))
    cxt['error'] = ''


def clickOperator(new_op, cxt, request):
    # Check for consecutive operators: only update the operator
    prev_click = cxt['prev_click']
    if prev_click == 'plus' or prev_click == 'minus' or \
       prev_click == 'times' or prev_click == 'divide':
        cxt['prev_op'] = new_op
        cxt['prev_click'] = new_op
        print('prev_op & prev_lick: ' + cxt['prev_op'])
        return

    # Compute the result
    prev_op = cxt['prev_op']
    prev_val = cxt['prev_val']
    new_val = cxt['new_val']

    result = 0
    if prev_op == 'equals':
        result = new_val
    elif prev_op == 'plus':
        result = prev_val + new_val
    elif prev_op == 'minus':
        result = prev_val - new_val
    elif prev_op == 'times':
        result = prev_val * new_val
    elif prev_op == 'divide':
        # Detect division by zero
        if new_val == 0:
            print('Division by zero')
            resetContext(cxt, 'Division by zero')
            return
        # Integer division using '//'
        result = prev_val // new_val
    print('result: ' + str(result))
    cxt['result'] = result

    # Update variables
    cxt['prev_val'] = result
    cxt['prev_op'] = new_op
    cxt['new_val'] = 0
    print('prev_val: ' + str(cxt['prev_val']) + ', prev_op: ' +
          str(cxt['prev_op']) + ', new_val: ' + str(cxt['new_val']))
    cxt['prev_click'] = new_op
    cxt['error'] = ''
