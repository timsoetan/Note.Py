from browser import bind, document, window

# nav bar buttons
add_note = document['add-note']
color_changer = document['color-changer']
note_search = document['note-search']
log_in = document['log-in']

# nav bar button icons
brand_icon = document['brand-icon']
add_note_icon = document['add-note-icon']
color_changer_icon = document['color-changer-icon']
note_search_icon = document['note-search-icon']
log_in_icon = document['log-in-icon']
try:
    sign_up_icon = document['sign-up-icon']
except KeyError:
    log_out_icon = document['log-out-icon']

# color changer bar
color_bar = document['color-bar']
active_color = document['active-color']
green_color_button = document['green-color-button']
yellow_color_button = document['yellow-color-button']
orange_color_button = document['orange-color-button']
purple_color_button = document['purple-color-button']
pink_color_button = document['pink-color-button']
blue_color_button = document['blue-color-button']

# search bar
search_bar = document['search-bar']
end_search_button = document['end-search-button']

# border colors
green_border_hex_code = '#A7CA8B'
yellow_border_hex_code = '#DBCE66'
orange_border_hex_code = '#DEAF77'
purple_border_hex_code = '#9167A2'
pink_border_hex_code = '#D98FAC'
blue_border_hex_code = '#71C2BD'


# animates the brand icon on hover
@bind('#brand', 'mouseover')
def rotate_brand_icon(event):
    brand_icon.classList.add('faa-shake')
    brand_icon.classList.add('animated')


# stops animation on the brand icon after hover
@bind('#brand', 'mouseout')
def reset_brand_icon(event):
    brand_icon.classList.remove('faa-shake')
    brand_icon.classList.remove('animated')


# animates the add note icon on hover
@bind('#add-note', 'mouseover')
def rotate_add_note_icon(event):
    add_note_icon.classList.add('faa-shake')
    add_note_icon.classList.add('animated')


# stops animation on the add not icon after hover
@bind('#add-note', 'mouseout')
def reset_add_note_icon(event):
    add_note_icon.classList.remove('faa-shake')
    add_note_icon.classList.remove('animated')


# animates the color changer icon on hover
@bind('#color-changer', 'mouseover')
def rotate_color_changer_icon(event):
    color_changer_icon.classList.add('faa-shake')
    color_changer_icon.classList.add('animated')


# stops animation on the color changer icon after hover
@bind('#color-changer', 'mouseout')
def reset_color_changer_icon(event):
    color_changer_icon.classList.remove('faa-shake')
    color_changer_icon.classList.remove('animated')


# animates the note search icon on hover
@bind('#note-search', 'mouseover')
def rotate_note_search_icon(event):
    note_search_icon.classList.add('faa-shake')
    note_search_icon.classList.add('animated')


# stops animation on the note search icon after hover
@bind('#note-search', 'mouseout')
def reset_note_search_icon(event):
    note_search_icon.classList.remove('faa-shake')
    note_search_icon.classList.remove('animated')


# animates the log in icon on hover
@bind('#log-in', 'mouseover')
def rotate_log_in_icon(event):
    log_in_icon.classList.add('faa-shake')
    log_in_icon.classList.add('animated')


# stops animation on the log in icon after hover
@bind('#log-in', 'mouseout')
def reset_log_in_icon(event):
    log_in_icon.classList.remove('faa-shake')
    log_in_icon.classList.remove('animated')


# animates the sign up icon on hover
@bind('#sign-up', 'mouseover')
def rotate_sign_up_icon(event):
    sign_up_icon.classList.add('faa-shake')
    sign_up_icon.classList.add('animated')


# stops animation on the sign up icon after hover
@bind('#sign-up', 'mouseout')
def reset_sign_up_icon(event):
    sign_up_icon.classList.remove('faa-shake')
    sign_up_icon.classList.remove('animated')


# animates the log out icon on hover
@bind('#log-out', 'mouseover')
def rotate_log_out_icon(event):
    log_out_icon.classList.add('faa-shake')
    log_out_icon.classList.add('animated')


# stops animation on the log out icon after hover
@bind('#log-out', 'mouseout')
def reset_log_out_icon(event):
    log_out_icon.classList.remove('faa-shake')
    log_out_icon.classList.remove('animated')


# changes the active note color to green
@bind('#green-color-button', 'click')
def change_color_to_green(event):
    green_hex_code = green_color_button.value

    on_color_selected(green_hex_code, green_border_hex_code)


# changes the active note color to yellow
@bind('#yellow-color-button', 'click')
def change_color_to_yellow(event):
    yellow_hex_code = yellow_color_button.value

    on_color_selected(yellow_hex_code, yellow_border_hex_code)


# changes the active note color to orange
@bind('#orange-color-button', 'click')
def change_color_to_orange(event):
    orange_hex_code = orange_color_button.value

    on_color_selected(orange_hex_code, orange_border_hex_code)


# changes the active note color to purple
@bind('#purple-color-button', 'click')
def change_color_to_pink(event):
    purple_hex_code = purple_color_button.value

    on_color_selected(purple_hex_code, purple_border_hex_code)


# changes the active note color to pink
@bind('#pink-color-button', 'click')
def change_color_to_pink(event):
    pink_hex_code = pink_color_button.value

    on_color_selected(pink_hex_code, pink_border_hex_code)


# changes the active note color to blue
@bind('#blue-color-button', 'click')
def change_color_to_orange(event):
    blue_hex_code = blue_color_button.value

    on_color_selected(blue_hex_code, blue_border_hex_code)


# sets new active note color and closes the color bar
def on_color_selected(color_hex_code, color_border_hex_code):
    active_color.style.background = color_hex_code
    active_color.style.borderColor = color_border_hex_code

    event = window.MouseEvent.new('click')

    color_changer.dispatchEvent(event)


# opens the color bar and closes any other open nav bars
@bind('#color-changer', 'click')
def show_color_bar(event):
    color_bar_display = color_bar.style.display
    search_bar_display = search_bar.style.display

    if search_bar_display == 'block':
        event = window.MouseEvent.new('click')

        end_search_button.dispatchEvent(event)

    if color_bar_display == 'none':
        color_bar.style.display = 'block'

        search_bar.style.display = 'none'

        note_search.classList.remove('active')

        color_changer.classList.add('active')
    else:
        color_bar.style.display = 'none'

        color_changer.classList.remove('active')


# opens the search bar and closes any other nav bars
@bind('#note-search', 'click')
def show_search_bar(event):
    search_bar_display = search_bar.style.display
    color_bar_display = color_bar.style.display

    if color_bar_display == 'block':
        event = window.MouseEvent.new('click')

        color_changer.dispatchEvent(event)

    if search_bar_display == 'none':
        search_bar.style.display = 'block'

        color_bar.style.display = 'none'

        color_changer.classList.remove('active')

        note_search.classList.add('active')
    else:
        search_bar.style.display = 'none'

        note_search.classList.remove('active')
