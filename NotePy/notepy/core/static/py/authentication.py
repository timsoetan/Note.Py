from browser import bind, document, window, timer, ajax
import re
import json

# sign-up form
sign_up_form = document['sign-up-form']
sign_up_first_name = document['sign-up-first-name']
sign_up_last_name = document['sign-up-last-name']
sign_up_email = document['sign-up-email']
sign_up_password = document['sign-up-password']
sign_up_button = document['sign-up-button']
sign_up_toast = document['sign-up-toast']
sign_up_progress = document['sign-up-progress']

# log-in form
log_in_form = document['log-in-form']
log_in_email = document['log-in-email']
log_in_password = document['log-in-password']
log_in_button = document['log-in-button']
log_in_toast = document['log-in-toast']
log_in_progress = document['log-in-progress']

# constants
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# bind log in button click to send log in ajax request to server
# handles input validation before data is sent to server
@bind('#log-in-button', 'click')
def log_in(event):
    email = log_in_email.value
    password = log_in_password.value

    if not email and not password:
        show_toast("You Didn't Enter Anything", "log in", "error")

        return
    elif not email:
        show_toast("You Didn't Enter Your Email", "log in", "error")

        return
    elif not password:
        show_toast("You Didn't Enter Your Password", "log in", "error")

        return
    else:
        req = ajax.Ajax()
        req.bind('loading', on_send_log_in)
        req.bind('complete', on_log_in)
        req.open('POST', '/log_in', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send({'email': email, 'password': password})


# resets the log in form when modal dialog is closed
@bind('#log-in-close', 'click')
def reset_log_in_form(event):
    log_in_form.reset()


# display progress bar in modal while ajax request is being sent to the server
def on_send_log_in(request):
    log_in_progress.style.display = 'block'


# handles the response sent by the server when the log in ajax request is
# completed
def on_log_in(request):
    log_in_progress.style.display = 'none'

    json_response = json.loads(request.text)

    if not json_response['success']:
        show_toast(json_response['message'], "log in", "server")
    else:
        show_toast(json_response['message'], "log in", "success")

        timer.set_timeout(go_to_home, 1000)


# bind sign up button click to send sign up ajax request to server
# handles input validation before data is sent to server
@bind('#sign-up-button', 'click')
def sign_up(event):
    first_name = sign_up_first_name.value
    last_name = sign_up_last_name.value
    email = sign_up_email.value
    password = sign_up_password.value

    if not first_name and not last_name and not email and not password:
        show_toast("You Didn't Enter Anything", "sign up", "error")

        return
    elif not first_name:
        show_toast("You Didn't Enter Your First Name", "sign up", "error")

        return
    elif not last_name:
        show_toast("You Didn't Enter Your Last Name", "sign up", "error")

        return
    elif not email:
        show_toast("You Didn't Enter An Email", "sign up", "error")

        return
    elif not password:
        show_toast("You Didn't Enter A Password", "sign up", "error")

        return
    elif not validate_name(first_name):
        show_toast("First Name Is Invalid", "sign up", "validate")

        return
    elif not validate_name(last_name):
        show_toast("Last Name Is Invalid", "sign up", "validate")

        return
    elif not validate_email(email):
        show_toast("Email Is Invalid", "sign up", "validate")

        return
    elif not validate_password(password):
        show_toast(
            "Password Must Have:<br>" +
            "At Least 8 Characters<br>" +
            "1 Number<br>" +
            "1 Uppercase Letter<br>" +
            "1 Special Character",
            "sign up",
            "validate")

        return
    else:
        req = ajax.Ajax()
        req.bind('loading', on_send_sign_up)
        req.bind('complete', on_sign_up)
        req.open('POST', '/sign_up', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send(
            {'first_name': first_name, 'last_name': last_name, 'email': email,
             'password': password})


# resets the sign up form when modal dialog is closed
@bind('#sign-up-close', 'click')
def reset_sign_up_form(event):
    sign_up_form.reset()


# display progress bar in modal while ajax request is being sent to the server
def on_send_sign_up(request):
    sign_up_progress.style.display = 'block'


# handles the response sent by the server when the sign ip ajax request is
# completed
def on_sign_up(request):
    sign_up_progress.style.display = 'none'

    json_response = json.loads(request.text)

    if not json_response['success']:
        show_toast(json_response['message'], "sign up", "server")
    else:
        show_toast(json_response['message'], "sign up", "success")

        timer.set_timeout(go_to_home, 1000)


# if log in or sign up ajax request was successful, render the user's home
# page
def go_to_home():
    window.location = '/home'


# displays any errors or messages directed at the user as a toast
def show_toast(response, toast_type, category):
    def end_sign_up_toast():
        sign_up_toast.classList.remove('show')
        sign_up_toast.classList.remove('validate')
        sign_up_toast.classList.remove('server')
        sign_up_toast.classList.remove('success')

    def end_log_in_toast():
        log_in_toast.classList.remove('show')
        log_in_toast.classList.remove('server')

    if toast_type == 'sign up':
        sign_up_toast.innerHTML = response

        if category == 'error':
            sign_up_toast.classList.add('show')

            timer.set_timeout(end_sign_up_toast, 3000)
        elif category == 'validate':
            sign_up_toast.classList.add('validate')
            sign_up_toast.classList.add('show')

            timer.set_timeout(end_sign_up_toast, 3000)
        elif category == 'server':
            sign_up_toast.classList.add('server')
            sign_up_toast.classList.add('show')

            timer.set_timeout(end_sign_up_toast, 3000)
        elif category == 'success':
            sign_up_toast.classList.add('success')
            sign_up_toast.classList.add('show')

            timer.set_timeout(end_sign_up_toast, 3000)
    elif toast_type == 'log in':
        log_in_toast.innerHTML = response

        if category == 'error':
            log_in_toast.classList.add('show')

            timer.set_timeout(end_log_in_toast, 3000)
        elif category == 'server':
            log_in_toast.classList.add('server')
            log_in_toast.classList.add('show')

            timer.set_timeout(end_log_in_toast, 3000)
        elif category == 'success':
            log_in_toast.classList.add('success')
            log_in_toast.classList.add('show')

            timer.set_timeout(end_log_in_toast, 3000)


# Helper functions #
# checks if a name only contains letters
def validate_name(name):
    return name.isalpha()


# checks if email adheres to basic email formatting
def validate_email(email):
    return EMAIL_REGEX.match(email)


# checks if password has at least 8 characters, 1 number, 1 uppercase
# character, 1 lowercase character and 1 special character
def validate_password(password):
    special_characters = ['!', '?', "#", "%", "@", "*", "(", ")", "~", ",",
                          ".", "<", ">", ":", ";", "\"", "\'", "{", "}", "[",
                          "]"]

    if len(password) < 8:
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char in special_characters for char in password):
        return False

    return True
