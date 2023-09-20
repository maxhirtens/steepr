# STEEPR

Steepr is:

- A companion app for Spotify users.
- A music-based countdown timer for steeping tea.
- Available at steepr.onrender.com

![The homepage](/static/images/Homepage.png)

### 1. Function

Most teas come with a recommended steeping time. Black tea might take 5 minutes, and green tea might take 2 minutes. But just setting a timer is boring. Steepr is a simple web app that allows you to choose a length of time and a musical genre, then listen to a random Spotify song that matches your criteria. When the song is over, your tea is ready!

### 2. Features

The homepage offers a form with a select field for the length of time, and a text field for genre. There are hundreds of genres available on Spotify; however you can also leave this field blank to select a random song.

Every combination of time plus genre is known as a 'Steep'. Once a user has signed up and logged in, they are able to name and save a Steep to their profile for later reuse. A Steep can be simply a time and genre, or saved with the exact track that is currently playing.

For example, if a user selects "4 minutes" and "rock", Steepr might begin playing "Under Pressure" by Queen. The user can name this combo as "Monday Morning Black Tea", and save it to their profile.

### 3. User Flow

The first step is to make sure a user is logged in to Spotify, otherwise full-length tracks will not play. Steepr is available to use now, but users must also be logged in to Steepr in order to save their Steeps. Once logged in, users are redirected to the homepage where they can see their saved Steeps as well as the search form. After form submission, all users are sent to the player page, which uses an embedded Spotify player for playback. If logged in, users then see options for saving Steeps below the embedded player.

![The player page](/static/images/Player.png)

### 4. API

The Spotify API is available with this base URL - 'https://api.spotify.com/v1/search'. Original attempts at creating Steepr used this URL directly, however for more robust authentication I decided to use a separate python library known as Spotipy (https://spotipy.readthedocs.io/en/2.21.0/).

### 5. Tech Stack

Steepr was created with: Python, Flask, Jinja, WTForms, Spotipy, SQLAlchemy, postgreSQL, and bcrypt.

### 6. Devs

You must create a .env file and log a SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET, using your personal Spotify API settings.
