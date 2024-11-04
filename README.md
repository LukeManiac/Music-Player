# Music Player

This Music Player application provides a user-friendly interface for managing and playing music files. Developed in Python using the `tkinter` library for the GUI and `pygame` for audio playback, this app supports multiple audio formats and includes features like looping, shuffling, and metadata display. Users can load songs into the playlist, control playback, view song metadata, and customize playback options such as looping mode.

## Features

The Music Player allows you to easily load multiple songs into a playlist. Using the built-in file dialog, you can select audio files with extensions `.mp3`, `.wav`, `.ogg`, and `.flac`, and they will be added to the playlist box, displaying just the filename. Playback controls include Play, Pause, Stop, Previous, Next, Shuffle, and Remove. Loop modes are selectable from a dropdown, offering "No Loop," "Single Loop," and "Loop All" options, providing flexibility in playback style.

## Metadata Display

In addition to playback, this application shows metadata for each song. When a song is played, metadata such as the song name, artist, album, genre, sample rate, and duration are displayed in a read-only text box. If album artwork is available, it is displayed alongside the metadata. This feature is achieved through the `mutagen` library, which extracts metadata tags, and `PIL` (Python Imaging Library) for displaying artwork images. The metadata frame offers a compact yet comprehensive view of song information.

## Playlist Management and Playback

The Music Player supports seamless playback and playlist management. The current song's position is displayed with a time slider that allows you to seek within the song, and labels show both the current time and duration. A threaded function manages the playback loop, updating the slider and labels in real-time. If looping is set to "Single Loop," the current song will replay automatically; if "Loop All" is selected, the player cycles through all songs in the playlist.

## Random and Selective Song Control

The Shuffle button randomizes the playlist order, allowing you to experience your music in a fresh sequence each time. For more control, the player also has dedicated buttons for moving to the next or previous song and removing selected songs from the playlist. To ensure a user-friendly experience, warning messages prompt you when attempting actions without songs in the playlist or without a song selected.

## Dependencies and Installation

The app requires Python libraries such as `pygame`, `tkinter`, `mutagen`, and `PIL` (from `Pillow`). To install these dependencies, use `pip install pygame mutagen pillow` in your terminal. Once dependencies are installed, run the `MusicPlayer.py` script to launch the application. The user interface adapts to various screen sizes with a responsive layout, providing an enjoyable experience on different devices.
