from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import JsonResponse
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import StickyNote

import json


# renders the splash page for the web app
def splash(request):
    # if user is already logged in redirect to user home page
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'splash.html')


# handles the ajax request send on the sign up form's submit button
# returns a json response detailing if the user was registered successfully
@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        # get registration details from request data
        first_name = request.POST['first_name']

        last_name = request.POST['last_name']

        email = request.POST['email']

        password = request.POST['password']

        # check is user with the request data's email exists in database
        try:
            user = get_user_model().objects.create_user(first_name=first_name,
                                                        last_name=last_name,
                                                        email=email,
                                                        password=password)
        except IntegrityError:
            result = {"success": False,
                      "message": "A User With That Email Exists Already"}

            return JsonResponse(result)

        # logs the newly registered user into the app
        login(request, user)

        result = {"success": True, "message": "Successfully Registered"}

        return JsonResponse(result)


# handles the ajax request send on the log in form's submit button
# returns a json response detailing if the user was logged in successfully
@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        # get log in details from request data
        email = request.POST['email']

        password = request.POST['password']

        user = authenticate(email=email, password=password)

        # check if a user with the request data's credentials is in the
        # database
        if user is None:
            result = {"success": False, "message": "Account Wasn't Found"}

            return JsonResponse(result)
        else:
            # logs the user into the app
            login(request, user)

            result = {"success": True, "message": "Welcome Back"}

            return JsonResponse(result)


# handles the ajax request to log a user out of the application
# returns a json response detailing if the user was logged out successfully
@csrf_exempt
def log_out(request):
    if request.method == 'POST':
        # logs the user out of the app
        logout(request)

        result = {"success": True, "message": "Goodbye"}

        return JsonResponse(result)


# renders a user's home page for the web app
# sends the user as json object
@login_required
def home(request):
    return render(request, "home.html")


# handles the ajax request to load a user's saved sticky notes
# returns a json response formatted as a list of sticky note-model dictionaries
# and the current logged in user
@csrf_exempt
def load_notes(request):
    if request.method == 'POST':
        user = request.user

        # check if a user is logged in
        if not user.is_authenticated:
            result = {"success": False}

            return JsonResponse(result)

        user_sticky_notes = StickyNote.objects.filter(creator=user)

        list_user_sticky_notes = list()

        for sticky_note in user_sticky_notes:
            list_user_sticky_notes.append(model_to_dict(sticky_note))

        result = {"success": True, "message": list_user_sticky_notes,
                  "user": model_to_dict(user)}

        return JsonResponse(result)


# handles the ajax request to create a user's sticky note
# returns a json response formatted as a sticky note-model dictionary
@csrf_exempt
def create_note(request):
    if request.method == 'POST':
        # get initial sticky note attributes from request data
        left = request.POST['left']

        top = request.POST['top']

        z_index = request.POST['z_index']

        sticky_note = StickyNote.objects.create(left=left,
                                                top=top,
                                                z_index=z_index,
                                                creator=request.user)

        result = {"success": True,
                  "message": model_to_dict(sticky_note)}

        return JsonResponse(result)


# handles the ajax request to save a user's sticky note
# returns a json response detailing if the note was saved successfully
@csrf_exempt
def save_note(request):
    if request.method == 'POST':
        # get updated sticky note attributes from request data
        left = request.POST['left']

        top = request.POST['top']

        z_index = request.POST['z_index']

        time_stamp = request.POST['time_stamp']

        text = request.POST['text']

        rotation_style = request.POST['rotation_style']

        note_color = request.POST['note_color']

        note_border_color = request.POST['note_border_color']

        pen_color = request.POST['pen_color']

        sticky_note_id = request.POST['id']

        StickyNote.objects.filter(id=sticky_note_id).update(
            left=left,
            top=top,
            z_index=z_index,
            time_stamp=time_stamp,
            text=text,
            rotation_style=rotation_style,
            note_color=note_color,
            note_border_color=note_border_color,
            pen_color=pen_color)

        result = {"success": True}

        return JsonResponse(result)


# handles the ajax request to remove a user's sticky note
# returns a json response detailing if the note was removed successfully
@csrf_exempt
def close_note(request):
    if request.method == 'POST':
        sticky_note_id = request.POST['id']

        StickyNote.objects.filter(id=sticky_note_id).delete()

        result = {"success": True}

        return JsonResponse(result)
