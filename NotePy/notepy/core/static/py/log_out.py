from browser import bind, document, window, timer, ajax
import json

# log-out form
log_out_yes_button = document['log-out-yes-button']
log_out_toast = document['log-out-toast']


# bind log out yes button click to send log out ajax request to server
@bind('#log-out-yes-button', 'click')
def log_out(event):
    req = ajax.Ajax()
    req.bind('complete', on_log_out)
    req.open('POST', '/log_out', True)
    req.send()


# handles the response sent by the server when the log out ajax request is
# completed
def on_log_out(request):
    json_response = json.loads(request.text)

    if not json_response['success']:
        show_toast(json_response['message'], 'log out', 'server')
    else:
        show_toast(json_response['message'], 'log out', 'success')

        timer.set_timeout(go_to_splash, 1000)


# if log out ajax request was successful, render the splash page
def go_to_splash():
    window.location = '/'


# displays any errors or messages directed at the user as a toast
def show_toast(response, toast_type, category):
    def end_log_out_toast():
        log_out_toast.classList.remove('show')
        log_out_toast.classList.remove('success')

    if toast_type == 'log out':
        log_out_toast.innerHTML = response

        if category == 'success':
            log_out_toast.classList.add('success')
            log_out_toast.classList.add('show')

            timer.set_timeout(end_log_out_toast, 3000)
