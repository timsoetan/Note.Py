# NotePy

NotePy is a web application for taking sticky notes similar to [Note.ly](https://note.ly/).

Anyone who accesses the website will be able to use all of the basic features such as creating, customizing and deleting notes but only registered users have the status of their note board saved.

## Prerequisites

This project uses MySQL as it's database management system so you'll have to set up a MySQL server on your computer for it to run.

1. Download [XAMPP](https://www.apachefriends.org/download.html) for your operating system.
2. Once downloaded, start the installer and make sure that MySQL is checked once you get to the **Select Components** prompt.
3. Continue through the installation steps and finally install XAMPP in an empty folder on your computer.
4. When the installation is complete, check the box that says "Do you want to start the Control Panel now?" and press the **Finish** button.
5. On the XAMPP Control Panel, press the **Start** button connected to the Apache module first and then press the **Start** button connected to the MySQL module.
6. When both the Apache and MySQL modules are running, press the **Admin** button connected to the MySQL module. This will take you to the admin page of your MySQL server.
7. On the MySQL admin page, press the **Databases** tab at the top and create a database named 'notepy'. 

The MySQL server is now running and we've successfully set up the database that will be linked to the Django configuration in the project.

## Installing

Now that we've created our MySQL server with the appropriate name, it should be linked to the Django configuration in the project.

After downloading the project, ```cd``` to the project's working directory and run the following commands in order:

```bash
pip install -r requirements.txt
```
```bash
python manage.py makemigrations core
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```

The project's address will be displayed in the terminal.

## Routes

### Splash | ""

Displays the basic layout of the website. At the top of the web page there's a navigation bar with buttons for creating a sticky note, changing the sticky note color, searching through created sticky notes, logging in and signing up.

### Log In | "/log_in"

Authenticates a user based on input credentials to give them access to the main app.

### Sign Up | "/sign_up"

Registers a user based on input credentials to give them access to the main app.

### Log Out | "/log_out"

Logs a user out of the main app.

### Home | "/home"

Displays a user's homepage. Here they can do everything they did on the splash page, but the status of their sticky note board is saved is saved when any changes are made.

### Load Notes | "/load_notes"

Loads a user's saved sticky notes when their homepage is loaded.

### Create Note | "/create_note"

Sends a request to the server to create a new sticky note for a registered user.

### Save Note | "/save_note"

Sends a request to the server to save the state of a user's sticky note that was recently updated.

### Close Note | "/close_note"

Sends a request to the server to have a user's sticky note deleted.

## Project Structure

The project uses Django for web frame-working and user authentication, MySQL as the database management system and Brython to write python scripts that can interact with Javascript's HTML DOM.

## Videos

[Project Walkthrough](https://drive.google.com/file/d/1jZX1jiSg67AA8kyIz9_NJGKAULzqGNWc/view?usp=sharing)

[Code Requirements Walkthrough](https://drive.google.com/file/d/142AJYFchDn7nEJHx199qfNgRWuiACeMj/view?usp=sharing)