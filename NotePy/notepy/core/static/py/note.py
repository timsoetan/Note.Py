from browser import bind, document, window, timer, ajax
from abc import ABC, abstractmethod
from datetime import datetime
import re
import random
import json

# global variables
notes = list()
logged_in = False
captured = None
highest_z = 0
highest_id = 0

# nav bar buttons
add_note = document['add-note']
color_changer = document['color-changer']
note_search = document['note-search']

# color changer bar
color_bar = document['color-bar']
active_color = document['active-color']

# search bar
search_bar = document['search-bar']
search_button = document['search-button']
end_search_button = document['end-search-button']
search_params = document['search-params']
results = document['results']

# note frame
note_frame = document["note-frame"]
try:
    note_progress = document['note-progress']
except KeyError:
    pass


# abstract sticky note class
# defines the basic behavior for all sticky notes
class AbstractStickyNote(ABC):
    def __init__(self):
        self.id = None

        self.note = None
        self.close_button = None
        self.dark_pen = None
        self.blue_pen = None
        self.red_pen = None
        self.edit_field = None
        self.time_stamp = None

        self.rotation_style = 0
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        self.mouse_move_handler = None
        self.mouse_up_handler = None

    def __contains__(self, text):
        return text in self.get_text().lower()

    def __repr__(self):
        sticky_note_dict = dict()

        sticky_note_dict['left'] = self.get_left()
        sticky_note_dict['top'] = self.get_top()
        sticky_note_dict['z_index'] = str(self.get_z_index())
        sticky_note_dict['time_stamp'] = self.get_time_stamp()
        sticky_note_dict['text'] = self.get_text()
        sticky_note_dict['rotation_style'] = str(self.get_rotation_style())
        sticky_note_dict['note_color'] = self.note.style.background
        sticky_note_dict['note_border_color'] = self.note.style.borderColor
        sticky_note_dict['pen_color'] = self.edit_field.style.color
        sticky_note_dict['id'] = self.get_id()

        return sticky_note_dict

    def set_note(self, note):
        self.note = note

        self.note.bind('mousedown', self.on_mouse_down)
        self.note.bind('click', self.on_note_click)

        self.id = self.note.id

    def set_close_button(self, close_button):
        self.close_button = close_button

        self.close_button.bind('click', self.close)

    def set_pen_color_changers(self, dark_pen, blue_pen, red_pen):
        self.dark_pen = dark_pen
        self.dark_pen.bind('click', self.on_dark_pen_click)

        self.blue_pen = blue_pen
        self.blue_pen.bind('click', self.on_blue_pen_click)

        self.red_pen = red_pen
        self.red_pen.bind('click', self.on_red_pen_click)

    def set_edit_field(self, edit_field):
        self.edit_field = edit_field

        self.edit_field.bind('blur', self.on_edit_field_blur)

    def set_time_stamp(self, time_stamp):
        self.time_stamp = time_stamp

        self.time_stamp.bind('mousedown', self.on_mouse_down)

    def get_time_stamp(self):
        return self.time_stamp.innerHTML

    def get_id(self):
        return self.id

    def get_rotation_style(self):
        return self.rotation_style

    def set_rotation_style(self, rotation_style):
        self.rotation_style = rotation_style

    def get_text(self):
        return self.edit_field.textContent

    def set_text(self, text):
        self.edit_field.innerHTML = text

    def get_left(self):
        return self.note.style.left

    def set_left(self, left):
        self.note.style.left = left

    def get_top(self):
        return self.note.style.top

    def set_top(self, top):
        self.note.style.top = top

    def get_z_index(self):
        return self.note.style.zIndex

    def set_z_index(self, z_index):
        self.note.style.zIndex = z_index

    def on_mouse_down(self, event):
        global highest_z
        global captured

        captured = self

        self.start_x = event.clientX - self.note.offsetLeft
        self.start_y = event.clientY - self.note.offsetTop
        self.note.style.zIndex = highest_z
        highest_z = highest_z + 1

        if self.mouse_move_handler is None:
            self.mouse_move_handler = self.on_mouse_move
            self.mouse_up_handler = self.on_mouse_up

        document.bind('mousemove', self.mouse_move_handler)
        document.bind('mouseup', self.mouse_up_handler)

    def on_mouse_move(self, event):
        global captured

        if self is not captured:
            return True

        width = note_frame.clientWidth
        height = note_frame.clientHeight - 74

        if event.clientX - self.start_x > 46 and \
                event.clientX - self.start_x + 190 < width - 46:
            self.set_left(str(event.clientX - self.start_x) + 'px')

        if event.clientY - self.start_y > 46 and \
                event.clientY - self.start_y + 190 < height - 46:
            self.set_top(str(event.clientY - self.start_y) + 'px')

        self.save()

    def on_mouse_up(self, event):
        document.unbind('mousemove', self.mouse_move_handler)
        document.unbind('mouseup', self.mouse_up_handler)

    def on_note_click(self, event):
        self.edit_field.focus()

        document.getSelection().collapseToEnd()

    def on_dark_pen_click(self, event):
        self.edit_field.style.color = "#343a40"

        self.save()

    def on_blue_pen_click(self, event):
        self.edit_field.style.color = "#3575D3"

        self.save()

    def on_red_pen_click(self, event):
        self.edit_field.style.color = "#FF6C4D"

        self.save()

    def on_edit_field_blur(self, event):
        self.edit_field.scrollTop = 0

        self.save()

    @abstractmethod
    def close(self, event):
        pass

    @abstractmethod
    def save(self):
        pass

    @staticmethod
    def modify_date(date):
        time_stamp = 'Last Updated ' + date.strftime("%B %d, %Y %I:%M %p")

        return time_stamp


# sticky note class for logged in users
# save and close methods are configured for database use
class DBStickyNote(AbstractStickyNote):
    def close(self, event):
        req = ajax.Ajax()
        req.bind('complete', self.on_close)
        req.open('POST', '/close_note', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send({'id': self.get_id()})

    def on_close(self, request):
        global notes

        note_frame.removeChild(self.note)

        notes.remove(self)

    def save(self):
        self.time_stamp.innerHTML = self.modify_date(datetime.now())

        req = ajax.Ajax()
        req.open('POST', '/save_note', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send(repr(self))


# sticky note class for anonymous users
# save and close methods are relative to local session
class NonDBStickyNote(AbstractStickyNote):
    def close(self, event):
        global notes

        note_frame.removeChild(self.note)

        notes.remove(self)

    def save(self):
        self.time_stamp.innerHTML = self.modify_date(datetime.now())


# build the sticky note using brython/javascript DOM model
def sticky_note_builder(left, top, z_index, sticky_note_id, time, text,
                        rotation_style, note_color, note_border_color,
                        pen_color):
    global logged_in

    # create stick note class based on user authentication
    if logged_in:
        sticky_note = DBStickyNote()
    else:
        sticky_note = NonDBStickyNote()

    # build note
    note = document.createElement('A')
    note.className = 'note'
    note.id = sticky_note_id
    note.style.left = left
    note.style.top = top
    note.style.zIndex = z_index
    if note_color is None:
        note.style.background = active_color.style.background
        note.style.borderColor = active_color.style.borderColor
    else:
        note.style.background = note_color
        note.style.borderColor = note_border_color

    if rotation_style is not 0:
        if rotation_style is 2:
            note.style.transform = f'rotate(4deg)'
        elif rotation_style is 3:
            note.style.transform = f'rotate(-4deg)'
        elif rotation_style is 4:
            note.style.transform = f'rotate(-4deg)'
        elif rotation_style is 5:
            note.style.transform = f'rotate(-4deg)'
    else:
        rotation_style = random.randint(1, 5)

        if rotation_style is 2:
            note.style.transform = f'rotate(4deg)'
        elif rotation_style is 3:
            note.style.transform = f'rotate(-4deg)'
        elif rotation_style is 4:
            note.style.transform = f'rotate(-4deg)'
        elif rotation_style is 5:
            note.style.transform = f'rotate(-4deg)'

    # build close button
    close_button = document.createElement('DIV')
    close_button.className = 'close-button'
    close_button.innerHTML = '<i class="fas fa-trash-alt"></i>'
    note.appendChild(close_button)

    # build pen color changer
    pen_color_changer = document.createElement('DIV')
    pen_color_changer.className = 'pen-color-changer'
    pen_color_changer.innerHTML = '<i class="fas fa-pencil-alt"></i>'

    dark_pen = document.createElement('DIV')
    dark_pen.className = 'dark'
    pen_color_changer.appendChild(dark_pen)

    blue_pen = document.createElement('DIV')
    blue_pen.className = 'blue'
    pen_color_changer.appendChild(blue_pen)

    red_pen = document.createElement('DIV')
    red_pen.className = 'red'
    pen_color_changer.appendChild(red_pen)

    note.appendChild(pen_color_changer)

    # build edit field
    edit_field = document.createElement('DIV')
    edit_field.className = 'edit-field'
    edit_field.attrs['contenteditable'] = 'true'
    edit_field.textContent = text
    if pen_color is not None:
        edit_field.style.color = pen_color
    else:
        edit_field.style.color = "#343a40"
    note.appendChild(edit_field)

    # build time stamp
    time_stamp = document.createElement('DIV')
    time_stamp.className = 'time-stamp'
    if time:
        time_stamp.innerHTML = time
    if note_color is None:
        time_stamp.style.background = active_color.style.borderColor
        time_stamp.style.borderColor = active_color.style.borderColor
    else:
        time_stamp.style.background = note_border_color
        time_stamp.style.borderColor = note_border_color
    note.appendChild(time_stamp)

    # display the note on screen
    note_frame.appendChild(note)

    # initialize the sticky note's values
    sticky_note.set_note(note)
    sticky_note.set_rotation_style(rotation_style)
    sticky_note.set_close_button(close_button)
    sticky_note.set_pen_color_changers(dark_pen, blue_pen, red_pen)
    sticky_note.set_edit_field(edit_field)
    sticky_note.set_time_stamp(time_stamp)

    # for logged in users
    # check if note is being built from add note button or loaded from
    # the database
    if not time:
        sticky_note.save()

    # add note to local list
    notes.append(sticky_note)


# bind add note button to create a new sticky note on the web page
# handles cases where on splash page or on a user's home page
@bind('#add-note', 'click')
def add_note(event):
    global logged_in
    global notes
    global highest_z
    global highest_id

    color_bar_display = color_bar.style.display
    search_bar_display = search_bar.style.display

    if color_bar_display == 'block':
        event = window.MouseEvent.new('click')

        color_changer.dispatchEvent(event)
    elif search_bar_display == 'block':
        event = window.MouseEvent.new('click')

        end_search_button.dispatchEvent(event)

    left = str(random.randint(48, 150)) + 'px'
    top = str(random.randint(48, 150)) + 'px'

    z_index = highest_z
    highest_z = highest_z + 1

    if logged_in:  # Add note to database
        req = ajax.Ajax()
        req.bind('complete', on_create_note)
        req.open('POST', '/create_note', True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send({'left': left, 'top': top, 'z_index': str(z_index)})
    else:
        sticky_note_id = highest_id
        highest_id = highest_id + 1

        sticky_note_builder(left, top, z_index, sticky_note_id,
                            None, '', 0, None, None,
                            None)


# handles the response sent by the server when the create note ajax request is
# completed
# once note is created it's built on the web page
def on_create_note(request):
    json_response = json.loads(request.text)

    if json_response['success']:
        sticky_note = json_response['message']

        left = sticky_note['left']
        top = sticky_note['top']
        z_index = sticky_note['z_index']
        sticky_note_id = sticky_note['id']

        sticky_note_builder(left, top, int(z_index), sticky_note_id, None,
                            '',
                            0, None, None, None)


# bind search button to search in the text fields of all notes on the web page
@bind('#search-button', 'click')
def search(event):
    global notes

    search_string = search_params.value

    if search_string is None:
        return

    cleaned_params = re.split(r'; |, |\*|\s|and', search_string)
    cleaned_params = [param for param in cleaned_params if param]

    if len(cleaned_params) < 1:
        return

    tmp_notes = list()

    for note in notes:
        for param in cleaned_params:
            if param.lower() in note:
                note.note.style.display = "block"

                tmp_notes.append(note)

                break
            elif note in tmp_notes:
                continue
            else:
                note.note.style.display = "none"

    results.style.display = 'block'

    if len(tmp_notes) is 1:
        results.innerHTML = 'Found ' + str(len(tmp_notes)) + ' Note'
    else:
        results.innerHTML = 'Found ' + str(len(tmp_notes)) + ' Notes'

    toggle_search_results(True)


# ends search session on web page
# displays any notes that were hidden by searching a specific keyword
@bind('#end-search-button', 'click')
def end_search(event):
    global notes

    for note in notes:
        note.note.style.display = 'block'

    toggle_search_results(False)


# handles when a search session is started or ended
def toggle_search_results(is_enabled):
    if is_enabled:
        search_params.value = ''

        end_search_button.style.display = 'block'
    else:
        search_bar.style.display = 'none'

        note_search.classList.remove('active')

        search_params.value = ''

        end_search_button.style.display = 'none'

        results.style.display = 'none'
        results.innerHTML = ''


# handles the response sent by the server when the load notes ajax request is
# completed
def on_load_notes(request):
    note_progress.style.display = 'none'

    json_response = json.loads(request.text)

    if json_response['success']:
        global logged_in
        global highest_z

        logged_in = True

        sticky_notes = json_response['message']

        for sticky_note in sticky_notes:
            left = sticky_note['left']

            top = sticky_note['top']

            z_index = sticky_note['z_index']

            time_stamp = sticky_note['time_stamp']

            text = sticky_note['text']

            rotation_style = sticky_note['rotation_style']

            note_color = sticky_note['note_color']

            note_border_color = sticky_note['note_border_color']

            pen_color = sticky_note['pen_color']

            sticky_note_id = sticky_note['id']

            sticky_note_builder(left, top, int(z_index), sticky_note_id,
                                time_stamp,
                                text,
                                int(rotation_style), note_color,
                                note_border_color,
                                pen_color)

            if highest_z < int(z_index):
                highest_z = int(z_index) + 1


# display progress bar while load notes ajax request is incomplete
def query_notes(request):
    note_progress.style.display = 'block'


# ajax request to load the notes of the logged in user onto the web page
# determines functionality of note class
def load_notes():
    req = ajax.Ajax()
    req.bind('loading', query_notes)
    req.bind('complete', on_load_notes)
    req.open('POST', '/load_notes', True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send()


# start ajax request to load notes on document load
load_notes()
